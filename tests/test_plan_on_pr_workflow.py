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


class TestTerraformPlanOnPRWorkflow:
    """Test suite for the Terraform Plan on PR workflow."""

    def test_workflow_triggers_on_pull_request(self, workflow_config):
        """Test that the workflow is configured to trigger on pull requests to main."""
        # PyYAML parses 'on' as boolean True
        trigger_key = 'on' if 'on' in workflow_config else True
        assert trigger_key in workflow_config
        assert 'pull_request' in workflow_config[trigger_key]
        assert 'main' in workflow_config[trigger_key]['pull_request']['branches']

    def test_workflow_has_correct_permissions(self, workflow_config):
        """Test that the workflow has the required permissions."""
        assert 'permissions' in workflow_config
        permissions = workflow_config['permissions']
        assert permissions['id-token'] == 'write'
        assert permissions['contents'] == 'read'
        assert permissions['pull-requests'] == 'write'

    def test_workflow_has_plan_job(self, workflow_config):
        """Test that the workflow contains a plan job."""
        assert 'jobs' in workflow_config
        assert 'plan' in workflow_config['jobs']
        assert workflow_config['jobs']['plan']['name'] == 'Terraform Plan'
        assert workflow_config['jobs']['plan']['runs-on'] == 'ubuntu-latest'

    def test_workflow_checkout_step_exists(self, workflow_config):
        """Test that the workflow includes a checkout step."""
        steps = workflow_config['jobs']['plan']['steps']
        checkout_step = next(
            (s for s in steps if s.get('uses', '').startswith('actions/checkout')),
            None
        )
        assert checkout_step is not None
        assert checkout_step['uses'] == 'actions/checkout@v4'

    def test_workflow_setup_terraform_step(self, workflow_config):
        """Test that the workflow sets up Terraform with the correct version."""
        steps = workflow_config['jobs']['plan']['steps']
        terraform_step = next(
            (s for s in steps if s.get('name') == 'Setup Terraform'),
            None
        )
        assert terraform_step is not None
        assert terraform_step['uses'] == 'hashicorp/setup-terraform@v3'
        assert terraform_step['with']['terraform_version'] == '1.6.6'

    def test_workflow_terraform_init_step(self, workflow_config):
        """Test that the workflow runs terraform init with backend disabled."""
        steps = workflow_config['jobs']['plan']['steps']
        init_step = next(
            (s for s in steps if s.get('name') == 'Terraform Init'),
            None
        )
        assert init_step is not None
        assert init_step['run'] == 'terraform init -backend=false'

    def test_workflow_terraform_plan_step_exists(self, workflow_config):
        """Test that the workflow executes terraform plan and saves output."""
        steps = workflow_config['jobs']['plan']['steps']
        plan_step = next(
            (s for s in steps if s.get('name') == 'Terraform Plan'),
            None
        )
        assert plan_step is not None
        assert plan_step['id'] == 'plan'
        assert 'terraform plan -no-color' in plan_step['run']
        assert 'tee plan.txt' in plan_step['run']
        assert plan_step['continue-on-error'] is True

    def test_workflow_posts_plan_to_pr_comment(self, workflow_config):
        """Test that the workflow posts the plan output to the PR as a comment."""
        steps = workflow_config['jobs']['plan']['steps']
        post_step = next(
            (s for s in steps if s.get('name') == 'Post Plan to PR'),
            None
        )
        assert post_step is not None
        assert post_step['uses'] == 'actions/github-script@v7'
        
        # Verify the script reads plan.txt
        script = post_step['with']['script']
        assert "fs.readFileSync('plan.txt', 'utf8')" in script
        assert "github.rest.issues.createComment" in script
        assert "context.issue.number" in script
        assert "context.repo.owner" in script
        assert "context.repo.repo" in script

    def test_workflow_comment_includes_plan_outcome(self, workflow_config):
        """Test that the PR comment includes the plan success/failure status."""
        steps = workflow_config['jobs']['plan']['steps']
        post_step = next(
            (s for s in steps if s.get('name') == 'Post Plan to PR'),
            None
        )
        script = post_step['with']['script']
        assert "'${{ steps.plan.outcome }}'" in script
        assert "❌ Plan failed" in script
        assert "✅ Plan succeeded" in script

    def test_workflow_handles_plan_truncation(self, workflow_config):
        """Test that the workflow truncates large plan output."""
        steps = workflow_config['jobs']['plan']['steps']
        post_step = next(
            (s for s in steps if s.get('name') == 'Post Plan to PR'),
            None
        )
        script = post_step['with']['script']
        assert "maxLen = 65000" in script
        assert "plan.length > maxLen" in script
        assert "plan.substring(0, maxLen)" in script
        assert "(truncated)" in script

    def test_workflow_fails_on_plan_failure(self, workflow_config):
        """Test that the workflow fails the PR check if terraform plan fails."""
        steps = workflow_config['jobs']['plan']['steps']
        fail_step = next(
            (s for s in steps if s.get('name') == 'Fail if plan failed'),
            None
        )
        assert fail_step is not None
        assert fail_step['if'] == "steps.plan.outcome == 'failure'"
        assert fail_step['run'] == 'exit 1'

    def test_workflow_uses_github_script_for_commenting(self, workflow_config):
        """Test that the workflow uses github-script action for PR comments."""
        steps = workflow_config['jobs']['plan']['steps']
        post_step = next(
            (s for s in steps if s.get('name') == 'Post Plan to PR'),
            None
        )
        assert post_step is not None
        assert 'github-script' in post_step['uses']
        assert 'script' in post_step['with']

    def test_workflow_plan_output_formatted_as_hcl(self, workflow_config):
        """Test that the plan output is formatted as HCL code block."""
        steps = workflow_config['jobs']['plan']['steps']
        post_step = next(
            (s for s in steps if s.get('name') == 'Post Plan to PR'),
            None
        )
        script = post_step['with']['script']
        assert "```hcl" in script
        assert "## 📋 Terraform Plan" in script
