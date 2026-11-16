"""Unit tests for the Terraform Plan on PR workflow."""

import os

import pytest
import yaml


@pytest.fixture
def workflow_path():
    """Return the path to the plan-on-pr.yml workflow file."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".github/workflows/plan-on-pr.yml"
    )


@pytest.fixture
def workflow_config(workflow_path):
    """Load and parse the workflow YAML file."""
    with open(workflow_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture
def plan_job(workflow_config):
    return workflow_config['jobs']['plan']


def _step(job, name):
    return next((s for s in job['steps'] if s.get('name') == name), None)


class TestTerraformPlanOnPRWorkflow:
    """Test suite for the Terraform Plan on PR workflow."""

    def test_workflow_triggers_on_pull_request(self, workflow_config):
        """Test that the workflow is configured to trigger on pull requests to main."""
        # PyYAML parses 'on' as boolean True
        trigger_key = 'on' if 'on' in workflow_config else True
        assert 'pull_request' in workflow_config[trigger_key]
        assert 'main' in workflow_config[trigger_key]['pull_request']['branches']

    def test_workflow_has_correct_permissions(self, workflow_config):
        """OIDC token for AWS, read code, write the PR comment - nothing more."""
        assert workflow_config['permissions'] == {
            'id-token': 'write',
            'contents': 'read',
            'pull-requests': 'write',
        }

    def test_workflow_has_plan_job(self, plan_job):
        assert plan_job['name'] == 'Terraform Plan'
        assert plan_job['runs-on'] == 'ubuntu-latest'

    def test_skips_fork_pull_requests(self, plan_job):
        """Fork PRs get no OIDC token; the job should skip, not fail."""
        assert plan_job['if'] == 'github.event.pull_request.head.repo.full_name == github.repository'

    def test_plans_both_stacks(self, plan_job):
        include = plan_job['strategy']['matrix']['include']
        assert {(e['stack'], e['dir']) for e in include} == {
            ('root', '.'),
            ('monitoring', 'monitoring/terraform'),
        }
        assert plan_job['strategy']['fail-fast'] is False

    def test_uses_explicit_bash_for_pipefail(self, plan_job):
        """Default shell has no pipefail, which would let `| tee` hide a failed plan."""
        assert plan_job['defaults']['run']['shell'] == 'bash'

    def test_workflow_checkout_step_exists(self, plan_job):
        checkout = next(s for s in plan_job['steps'] if s.get('uses', '').startswith('actions/checkout'))
        assert checkout['uses'] == 'actions/checkout@v7'

    def test_workflow_setup_terraform_step(self, plan_job):
        step = _step(plan_job, 'Setup Terraform')
        assert step['uses'] == 'hashicorp/setup-terraform@v4'
        assert step['with']['terraform_version'] == '1.17.2'

    def test_authenticates_with_oidc_plan_role(self, plan_job):
        step = next(s for s in plan_job['steps'] if s.get('uses', '').startswith('aws-actions/configure-aws-credentials'))
        assert step['uses'] == 'aws-actions/configure-aws-credentials@v6'
        assert step['with']['role-to-assume'] == '${{ secrets.AWS_PLAN_ROLE_ARN }}'
        assert step['with']['mask-aws-account-id'] is True
        assert 'aws-access-key-id' not in step['with']

    def test_workflow_terraform_init_step(self, plan_job):
        """Init against real state; bucket comes from a repo variable."""
        step = _step(plan_job, 'Terraform Init')
        assert '-backend=false' not in step['run']
        assert '-backend-config="bucket=${TF_STATE_BUCKET}"' in step['run']
        assert plan_job['env']['TF_STATE_BUCKET'] == '${{ vars.TF_STATE_BUCKET }}'

    def test_workflow_terraform_plan_step_exists(self, plan_job):
        step = _step(plan_job, 'Terraform Plan')
        assert step['id'] == 'plan'
        assert 'terraform plan' in step['run']
        assert '-no-color' in step['run']
        assert '-lock-timeout=' in step['run']
        assert 'tee "$PLAN_FILE"' in step['run']
        assert step['continue-on-error'] is True

    def test_redacts_account_id_before_commenting(self, plan_job):
        names = [s.get('name') for s in plan_job['steps']]
        assert names.index('Redact account ID from plan text') < names.index('Post Plan to PR')
        assert 'sed -i' in _step(plan_job, 'Redact account ID from plan text')['run']

    def test_workflow_posts_plan_to_pr_comment(self, plan_job):
        step = _step(plan_job, 'Post Plan to PR')
        assert step['uses'] == 'actions/github-script@v9'
        script = step['with']['script']
        assert "fs.readFileSync(process.env.PLAN_FILE, 'utf8')" in script
        assert "await github.rest.issues.createComment" in script
        assert "context.issue.number" in script

    def test_workflow_comment_includes_plan_outcome(self, plan_job):
        """Outcome is passed via env, not interpolated into the script."""
        step = _step(plan_job, 'Post Plan to PR')
        assert step['env']['PLAN_OUTCOME'] == '${{ steps.plan.outcome }}'
        script = step['with']['script']
        assert '${{' not in script
        assert "❌ Plan failed" in script
        assert "✅ Plan succeeded" in script

    def test_workflow_handles_plan_truncation(self, plan_job):
        script = _step(plan_job, 'Post Plan to PR')['with']['script']
        assert "plan.length > maxLen" in script
        assert "(truncated)" in script

    def test_workflow_fails_on_plan_failure(self, plan_job):
        step = _step(plan_job, 'Fail if plan failed')
        assert step['if'] == "steps.plan.outcome == 'failure'"
        assert step['run'] == 'exit 1'

    def test_workflow_plan_output_formatted_as_hcl(self, plan_job):
        script = _step(plan_job, 'Post Plan to PR')['with']['script']
        assert "```hcl" in script
        assert "## 📋 Terraform Plan" in script
