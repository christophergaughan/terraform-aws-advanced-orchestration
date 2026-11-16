"""Unit tests for the validate and approval-gated apply/destroy workflows,
plus repo-wide guards on how Terraform workflows authenticate to AWS."""

import glob
import os

import pytest
import yaml

WORKFLOWS = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".github", "workflows")
TERRAFORM_WORKFLOWS = ["terraform.yml", "validate.yml", "plan-on-pr.yml", "terraform-apply.yml", "lint.yml"]


def _load(name):
    with open(os.path.join(WORKFLOWS, name), "r") as f:
        return yaml.safe_load(f)


def _on(config):
    # PyYAML parses the bare key `on` as boolean True
    return config["on"] if "on" in config else config[True]


def _step(job, name):
    return next((s for s in job["steps"] if s.get("name") == name), None)


class TestValidateWorkflow:

    @pytest.fixture
    def validate(self):
        return _load("validate.yml")

    def test_runs_on_push_to_main_and_prs(self, validate):
        on = _on(validate)
        assert "main" in on["push"]["branches"]
        assert "pull_request" in on

    def test_validates_every_stack(self, validate):
        dirs = {job["with"]["working-directory"] for job in validate["jobs"].values()}
        assert dirs == {".", "monitoring/terraform", "bootstrap"}

    def test_uses_local_reusable_workflow(self, validate):
        for job in validate["jobs"].values():
            assert job["uses"] == "./.github/workflows/terraform.yml"

    def test_needs_no_secrets(self, validate):
        for job in validate["jobs"].values():
            assert "secrets" not in job


class TestReusableValidateWorkflow:

    @pytest.fixture
    def job(self):
        return _load("terraform.yml")["jobs"]["validate"]

    def test_is_workflow_call_only(self):
        assert set(_on(_load("terraform.yml"))) == {"workflow_call"}

    def test_init_without_backend(self, job):
        assert _step(job, "Terraform Init")["run"] == "terraform init -input=false -backend=false"

    def test_runs_mocked_plan_tests(self, job):
        assert _step(job, "Terraform Test (mocked AWS)")["run"] == "terraform test"

    def test_no_aws_credentials(self, job):
        assert not any("configure-aws-credentials" in s.get("uses", "") for s in job["steps"])


class TestApplyWorkflow:

    @pytest.fixture
    def wf(self):
        return _load("terraform-apply.yml")

    def test_manual_trigger_only(self, wf):
        assert set(_on(wf)) == {"workflow_dispatch"}

    def test_action_choices(self, wf):
        assert _on(wf)["workflow_dispatch"]["inputs"]["action"]["options"] == ["apply", "destroy"]

    def test_root_stack_not_offered_until_placeholders_replaced(self, wf):
        assert _on(wf)["workflow_dispatch"]["inputs"]["stack"]["options"] == ["monitoring"]

    def test_permissions_are_minimal(self, wf):
        assert wf["permissions"] == {"id-token": "write", "contents": "read", "actions": "read"}

    def test_one_run_per_stack(self, wf):
        assert wf["concurrency"]["cancel-in-progress"] is False
        assert "inputs.stack" in wf["concurrency"]["group"]

    def test_plan_job_runs_only_on_main(self, wf):
        assert wf["jobs"]["plan"]["if"] == "github.ref == 'refs/heads/main'"

    def test_plan_job_checks_approval_gate_first(self, wf):
        first = wf["jobs"]["plan"]["steps"][0]
        assert first["name"] == "Require approval gate on aws-apply"
        assert "required_reviewers" in first["run"]

    def test_plan_job_uses_read_only_role(self, wf):
        creds = next(s for s in wf["jobs"]["plan"]["steps"] if "configure-aws-credentials" in s.get("uses", ""))
        assert creds["with"]["role-to-assume"] == "${{ secrets.AWS_PLAN_ROLE_ARN }}"

    def test_apply_job_is_environment_gated(self, wf):
        apply = wf["jobs"]["apply"]
        assert apply["environment"] == "aws-apply"
        assert apply["needs"] == "plan"
        assert apply["if"] == "needs.plan.outputs.has_changes == 'true'"

    def test_apply_job_uses_apply_role(self, wf):
        creds = next(s for s in wf["jobs"]["apply"]["steps"] if "configure-aws-credentials" in s.get("uses", ""))
        assert creds["with"]["role-to-assume"] == "${{ secrets.AWS_APPLY_ROLE_ARN }}"

    def test_apply_refuses_if_plan_changed_since_approval(self, wf):
        run = _step(wf["jobs"]["apply"], "Terraform Plan (saved)")["run"]
        assert '"$summary" != "$APPROVED_SUMMARY"' in run
        assert "-out=tfplan" in run

    def test_applies_the_saved_plan(self, wf):
        assert _step(wf["jobs"]["apply"], "Terraform Apply")["run"].endswith(" tfplan")

    def test_no_plan_artifacts_in_public_repo(self, wf):
        for job in wf["jobs"].values():
            assert not any("upload-artifact" in s.get("uses", "") for s in job["steps"])


class TestTerraformWorkflowAuth:
    """Terraform workflows authenticate with OIDC only - no static AWS keys."""

    @pytest.mark.parametrize("name", TERRAFORM_WORKFLOWS)
    def test_no_static_aws_keys(self, name):
        with open(os.path.join(WORKFLOWS, name), "r") as f:
            text = f.read()
        assert "AWS_ACCESS_KEY_ID" not in text
        assert "AWS_SECRET_ACCESS_KEY" not in text

    def test_removed_workflows_stay_removed(self):
        present = {os.path.basename(p) for p in glob.glob(os.path.join(WORKFLOWS, "*.yml"))}
        assert not present & {"deploy.yml", "deploy-monitoring.yml", "destroy-monitoring.yml"}
