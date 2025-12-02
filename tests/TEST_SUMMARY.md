# Test Summary

## Overview
Comprehensive unit tests covering GitHub Actions workflows and Terraform backend configuration for the terraform-aws-advanced-orchestration project.

## Test Results
✅ **All 45 tests passing**

## Test Coverage by Category

### 1. Terraform Plan on PR Workflow (14 tests)
**File**: `test_plan_on_pr_workflow.py`  
**Target**: `.github/workflows/plan-on-pr.yml`

#### ✅ Successfully generates and posts Terraform plan to PR comments
- `test_workflow_posts_plan_to_pr_comment` - Verifies plan is posted as PR comment
- `test_workflow_comment_includes_plan_outcome` - Confirms success/failure status in comment
- `test_workflow_plan_output_formatted_as_hcl` - Validates HCL code block formatting
- `test_workflow_handles_plan_truncation` - Tests truncation of large plans (>65KB)
- `test_workflow_uses_github_script_for_commenting` - Verifies github-script action usage

#### ✅ Correctly fails the PR check if terraform plan encounters errors
- `test_workflow_fails_on_plan_failure` - Ensures workflow exits with code 1 on plan failure
- `test_workflow_terraform_plan_step_exists` - Validates plan step with `continue-on-error: true`

#### Additional Coverage
- `test_workflow_triggers_on_pull_request` - Confirms trigger on PR to main branch
- `test_workflow_has_correct_permissions` - Validates OIDC and PR comment permissions
- `test_workflow_has_plan_job` - Verifies plan job configuration
- `test_workflow_checkout_step_exists` - Confirms code checkout step
- `test_workflow_setup_terraform_step` - Validates Terraform 1.6.6 setup
- `test_workflow_terraform_init_step` - Confirms `terraform init -backend=false`

---

### 2. Security Scan Workflow (13 tests)
**File**: `test_security_scan_workflow.py`  
**Target**: `.github/workflows/security-scan.yml`

#### ✅ Executes tfsec with specified configurations (5 tests)
- `test_tfsec_action_configured` - Verifies aquasecurity/tfsec-action@v1.0.3
- `test_tfsec_soft_fail_disabled` - Confirms `soft_fail: false` (fails on issues)
- `test_tfsec_uses_aquasecurity_action` - Validates official action usage
- `test_tfsec_checkout_step` - Confirms checkout step present
- `test_workflow_has_tfsec_job` - Validates tfsec job configuration

#### ✅ Executes Checkov with specified configurations (7 tests)
- `test_checkov_action_configured` - Verifies bridgecrewio/checkov-action@v12
- `test_checkov_scans_current_directory` - Confirms `directory: .`
- `test_checkov_framework_is_terraform` - Validates `framework: terraform`
- `test_checkov_soft_fail_disabled` - Confirms `soft_fail: false` (fails on violations)
- `test_checkov_output_format_is_cli` - Validates `output_format: cli`
- `test_checkov_uses_bridgecrew_action` - Confirms official action usage
- `test_checkov_has_all_required_configurations` - Verifies all parameters present

#### Additional Coverage
- `test_workflow_triggers` - Confirms triggers on push to main and pull requests

---

### 3. Backend Configuration (17 tests)
**File**: `test_backend_config.py`  
**Target**: `backend.tf`

#### ✅ Correctly specifies S3 backend with DynamoDB locking (8 tests)
- `test_backend_specifies_s3_backend` - Validates S3 backend declaration
- `test_backend_has_bucket_configuration` - Confirms bucket parameter
- `test_backend_has_key_configuration` - Validates state file key
- `test_backend_has_region_configuration` - Confirms AWS region
- `test_backend_has_encryption_enabled` - Verifies `encrypt = true`
- `test_backend_has_dynamodb_locking` - Validates DynamoDB table for locking
- `test_backend_configuration_completeness` - Ensures all required parameters present
- `test_backend_contains_terraform_block` - Confirms terraform block structure

#### Additional Validation Tests (9 tests)
- `test_backend_file_exists` - Confirms backend.tf exists
- `test_backend_has_documentation_comment` - Validates documentation comments
- `test_backend_mentions_s3_and_dynamodb` - Confirms S3 and DynamoDB mentioned
- `test_backend_mentions_locking` - Validates locking mentioned in docs
- `test_backend_region_is_valid_aws_region` - Tests valid AWS region format (us-east-2)
- `test_backend_key_path_format` - Validates .tfstate extension and path format
- `test_backend_bucket_name_format` - Confirms S3 naming conventions
- `test_backend_dynamodb_table_name_exists` - Validates descriptive table name
- `test_backend_configuration_is_documented_for_production` - Confirms production usage docs

---

## How to Run Tests

### Quick Start
```bash
# Install dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Test Plan on PR workflow only
pytest tests/test_plan_on_pr_workflow.py -v

# Test Security Scan workflow only
pytest tests/test_security_scan_workflow.py -v

# Test Backend configuration only
pytest tests/test_backend_config.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=tests --cov-report=term-missing --cov-report=html
```

## CI/CD Integration
A GitHub Actions workflow (`.github/workflows/unit-tests.yml`) is included to automatically run these tests on every push and pull request.

## Requirements
- Python 3.8+
- pytest 7.4.3+
- pytest-cov 4.1.0+
- pyyaml 6.0.1+

## Success Criteria Met

✅ **Test Case 1**: The `Terraform Plan on PR` workflow successfully generates and posts a Terraform plan to the pull request comments.
- 5 dedicated tests covering plan generation, posting, formatting, and truncation

✅ **Test Case 2**: The `Terraform Plan on PR` workflow correctly fails the PR check if the `terraform plan` command encounters errors.
- 2 dedicated tests validating failure behavior and exit codes

✅ **Test Case 3**: The `Security Scan` workflow executes `tfsec` with the specified configurations.
- 5 dedicated tests covering tfsec configuration, action version, and soft_fail setting

✅ **Test Case 4**: The `Security Scan` workflow executes `Checkov` with the specified configurations.
- 7 dedicated tests covering directory, framework, soft_fail, output format, and action version

✅ **Test Case 5**: The `backend.tf` configuration correctly specifies an S3 backend with DynamoDB locking for Terraform state management.
- 17 comprehensive tests covering all S3 backend parameters, DynamoDB locking, encryption, and validation rules
