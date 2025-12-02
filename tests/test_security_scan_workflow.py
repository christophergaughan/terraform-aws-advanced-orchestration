"""Unit tests for the Security Scan workflow."""

import os
import pytest
import yaml


@pytest.fixture
def workflow_path():
    """Return the path to the security-scan.yml workflow file."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".github/workflows/security-scan.yml"
    )


@pytest.fixture
def workflow_config(workflow_path):
    """Load and parse the workflow YAML file."""
    with open(workflow_path, 'r') as f:
        return yaml.safe_load(f)


class TestSecurityScanWorkflow:
    """Test suite for the Security Scan workflow."""

    def test_workflow_triggers(self, workflow_config):
        """Test that the workflow triggers on push to main and pull requests."""
        # PyYAML parses 'on' as boolean True
        trigger_key = 'on' if 'on' in workflow_config else True
        assert trigger_key in workflow_config
        assert 'push' in workflow_config[trigger_key]
        assert 'pull_request' in workflow_config[trigger_key]
        assert 'main' in workflow_config[trigger_key]['push']['branches']

    def test_workflow_has_tfsec_job(self, workflow_config):
        """Test that the workflow contains a tfsec job."""
        assert 'jobs' in workflow_config
        assert 'tfsec' in workflow_config['jobs']
        assert workflow_config['jobs']['tfsec']['name'] == 'tfsec'
        assert workflow_config['jobs']['tfsec']['runs-on'] == 'ubuntu-latest'

    def test_workflow_has_checkov_job(self, workflow_config):
        """Test that the workflow contains a Checkov job."""
        assert 'jobs' in workflow_config
        assert 'checkov' in workflow_config['jobs']
        assert workflow_config['jobs']['checkov']['name'] == 'Checkov'
        assert workflow_config['jobs']['checkov']['runs-on'] == 'ubuntu-latest'


class TestTfsecJob:
    """Test suite for the tfsec job configuration."""

    def test_tfsec_checkout_step(self, workflow_config):
        """Test that tfsec job includes checkout step."""
        steps = workflow_config['jobs']['tfsec']['steps']
        checkout_step = next(
            (s for s in steps if s.get('uses', '').startswith('actions/checkout')),
            None
        )
        assert checkout_step is not None
        assert checkout_step['uses'] == 'actions/checkout@v4'

    def test_tfsec_action_configured(self, workflow_config):
        """Test that tfsec action is configured with correct version and settings."""
        steps = workflow_config['jobs']['tfsec']['steps']
        tfsec_step = next(
            (s for s in steps if s.get('name') == 'tfsec'),
            None
        )
        assert tfsec_step is not None
        assert tfsec_step['uses'] == 'aquasecurity/tfsec-action@v1.0.3'

    def test_tfsec_soft_fail_disabled(self, workflow_config):
        """Test that tfsec is configured to fail on issues (soft_fail=false)."""
        steps = workflow_config['jobs']['tfsec']['steps']
        tfsec_step = next(
            (s for s in steps if s.get('name') == 'tfsec'),
            None
        )
        assert tfsec_step is not None
        assert 'with' in tfsec_step
        assert tfsec_step['with']['soft_fail'] is False

    def test_tfsec_uses_aquasecurity_action(self, workflow_config):
        """Test that the workflow uses the official aquasecurity tfsec action."""
        steps = workflow_config['jobs']['tfsec']['steps']
        tfsec_step = next(
            (s for s in steps if s.get('name') == 'tfsec'),
            None
        )
        assert 'aquasecurity/tfsec-action' in tfsec_step['uses']


class TestCheckovJob:
    """Test suite for the Checkov job configuration."""

    def test_checkov_checkout_step(self, workflow_config):
        """Test that Checkov job includes checkout step."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkout_step = next(
            (s for s in steps if s.get('uses', '').startswith('actions/checkout')),
            None
        )
        assert checkout_step is not None
        assert checkout_step['uses'] == 'actions/checkout@v4'

    def test_checkov_action_configured(self, workflow_config):
        """Test that Checkov action is configured with correct version."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        assert checkov_step['uses'] == 'bridgecrewio/checkov-action@v12'

    def test_checkov_scans_current_directory(self, workflow_config):
        """Test that Checkov is configured to scan the current directory."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        assert 'with' in checkov_step
        assert checkov_step['with']['directory'] == '.'

    def test_checkov_framework_is_terraform(self, workflow_config):
        """Test that Checkov is configured to scan Terraform framework."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        assert checkov_step['with']['framework'] == 'terraform'

    def test_checkov_soft_fail_disabled(self, workflow_config):
        """Test that Checkov is configured to fail on issues (soft_fail=false)."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        assert checkov_step['with']['soft_fail'] is False

    def test_checkov_output_format_is_cli(self, workflow_config):
        """Test that Checkov output format is set to CLI."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        assert checkov_step['with']['output_format'] == 'cli'

    def test_checkov_uses_bridgecrew_action(self, workflow_config):
        """Test that the workflow uses the official bridgecrewio Checkov action."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert 'bridgecrewio/checkov-action' in checkov_step['uses']

    def test_checkov_has_all_required_configurations(self, workflow_config):
        """Test that Checkov has all required configuration parameters."""
        steps = workflow_config['jobs']['checkov']['steps']
        checkov_step = next(
            (s for s in steps if s.get('name') == 'Checkov'),
            None
        )
        assert checkov_step is not None
        with_config = checkov_step['with']
        
        # Verify all required configurations are present
        assert 'directory' in with_config
        assert 'framework' in with_config
        assert 'soft_fail' in with_config
        assert 'output_format' in with_config
