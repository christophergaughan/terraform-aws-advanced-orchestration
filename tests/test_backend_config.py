"""Unit tests for the backend.tf Terraform configuration."""

import os
import re
import pytest


@pytest.fixture
def backend_file_path():
    """Return the path to the backend.tf file."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "backend.tf"
    )


@pytest.fixture
def backend_content(backend_file_path):
    """Load the backend.tf file content."""
    with open(backend_file_path, 'r') as f:
        return f.read()


class TestBackendConfiguration:
    """Test suite for the backend.tf configuration."""

    def test_backend_file_exists(self, backend_file_path):
        """Test that the backend.tf file exists."""
        assert os.path.exists(backend_file_path)
        assert os.path.isfile(backend_file_path)

    def test_backend_contains_terraform_block(self, backend_content):
        """Test that the backend configuration contains a terraform block."""
        # Check for terraform block (commented or uncommented)
        terraform_block_pattern = r'#?\s*terraform\s*\{'
        assert re.search(terraform_block_pattern, backend_content) is not None

    def test_backend_specifies_s3_backend(self, backend_content):
        """Test that the backend configuration specifies an S3 backend."""
        # Check for S3 backend declaration (commented or uncommented)
        s3_backend_pattern = r'#?\s*backend\s+"s3"\s*\{'
        assert re.search(s3_backend_pattern, backend_content) is not None

    def test_backend_has_bucket_configuration(self, backend_content):
        """Test that the backend configuration includes a bucket parameter."""
        # Check for bucket parameter (commented or uncommented)
        bucket_pattern = r'#?\s*bucket\s*=\s*"[^"]*"'
        assert re.search(bucket_pattern, backend_content) is not None

    def test_backend_has_key_configuration(self, backend_content):
        """Test that the backend configuration includes a key parameter."""
        # Check for key parameter (commented or uncommented)
        key_pattern = r'#?\s*key\s*=\s*"[^"]*"'
        assert re.search(key_pattern, backend_content) is not None

    def test_backend_has_region_configuration(self, backend_content):
        """Test that the backend configuration includes a region parameter."""
        # Check for region parameter (commented or uncommented)
        region_pattern = r'#?\s*region\s*=\s*"[^"]*"'
        assert re.search(region_pattern, backend_content) is not None

    def test_backend_has_encryption_enabled(self, backend_content):
        """Test that the backend configuration enables encryption."""
        # Check for encrypt parameter set to true (commented or uncommented)
        encrypt_pattern = r'#?\s*encrypt\s*=\s*true'
        assert re.search(encrypt_pattern, backend_content) is not None

    def test_backend_has_dynamodb_locking(self, backend_content):
        """Test that the backend configuration includes DynamoDB table for state locking."""
        # Check for dynamodb_table parameter (commented or uncommented)
        dynamodb_pattern = r'#?\s*dynamodb_table\s*=\s*"[^"]*"'
        assert re.search(dynamodb_pattern, backend_content) is not None

    def test_backend_configuration_completeness(self, backend_content):
        """Test that the backend configuration includes all required parameters for S3 + DynamoDB."""
        # Verify all essential S3 backend parameters are present
        required_params = [
            r'#?\s*bucket\s*=',
            r'#?\s*key\s*=',
            r'#?\s*region\s*=',
            r'#?\s*encrypt\s*=',
            r'#?\s*dynamodb_table\s*='
        ]
        
        for param_pattern in required_params:
            assert re.search(param_pattern, backend_content) is not None, \
                f"Missing required parameter: {param_pattern}"

    def test_backend_has_documentation_comment(self, backend_content):
        """Test that the backend configuration includes documentation comments."""
        # Check for comments indicating this is for remote state
        assert 'Remote State' in backend_content or 'remote state' in backend_content.lower()

    def test_backend_mentions_s3_and_dynamodb(self, backend_content):
        """Test that the backend documentation mentions S3 and DynamoDB."""
        content_lower = backend_content.lower()
        assert 's3' in content_lower
        assert 'dynamodb' in content_lower or 'dynamo' in content_lower

    def test_backend_mentions_locking(self, backend_content):
        """Test that the backend documentation mentions state locking."""
        content_lower = backend_content.lower()
        assert 'lock' in content_lower

    def test_backend_region_is_valid_aws_region(self, backend_content):
        """Test that the region specified is a valid AWS region format."""
        region_match = re.search(r'region\s*=\s*"([^"]+)"', backend_content)
        if region_match:
            region = region_match.group(1)
            # Valid AWS region format: us-east-1, eu-west-2, etc.
            region_pattern = r'^[a-z]{2}-[a-z]+-\d{1}$'
            assert re.match(region_pattern, region), \
                f"Region '{region}' does not match valid AWS region format"

    def test_backend_key_path_format(self, backend_content):
        """Test that the key parameter uses a proper path format."""
        key_match = re.search(r'key\s*=\s*"([^"]+)"', backend_content)
        if key_match:
            key = key_match.group(1)
            # Key should end with .tfstate
            assert key.endswith('.tfstate'), \
                f"Key '{key}' should end with .tfstate"
            # Key should contain a path separator or be a simple filename
            assert '/' in key or key == 'terraform.tfstate', \
                f"Key '{key}' should include a path for organization"

    def test_backend_bucket_name_format(self, backend_content):
        """Test that the bucket name follows AWS S3 naming conventions."""
        bucket_match = re.search(r'bucket\s*=\s*"([^"]+)"', backend_content)
        if bucket_match:
            bucket = bucket_match.group(1)
            # S3 bucket names should be lowercase and can contain hyphens
            # This is a basic check; full S3 naming rules are more complex
            assert bucket.islower() or '-' in bucket, \
                f"Bucket name '{bucket}' should follow S3 naming conventions"

    def test_backend_dynamodb_table_name_exists(self, backend_content):
        """Test that a DynamoDB table name is specified."""
        dynamodb_match = re.search(r'dynamodb_table\s*=\s*"([^"]+)"', backend_content)
        if dynamodb_match:
            table_name = dynamodb_match.group(1)
            assert len(table_name) > 0, "DynamoDB table name should not be empty"
            # Table name should be descriptive
            assert 'lock' in table_name.lower() or 'state' in table_name.lower(), \
                f"DynamoDB table name '{table_name}' should indicate its purpose"

    def test_backend_configuration_is_documented_for_production(self, backend_content):
        """Test that the backend configuration mentions production usage."""
        content_lower = backend_content.lower()
        assert 'production' in content_lower or 'uncomment' in content_lower, \
            "Backend configuration should mention production usage or activation instructions"
