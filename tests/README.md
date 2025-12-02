# Unit Tests

This directory contains unit tests for the Terraform AWS Advanced Orchestration project.

## Test Coverage

### 1. Terraform Plan on PR Workflow (`test_plan_on_pr_workflow.py`)
Tests for the `.github/workflows/plan-on-pr.yml` workflow:
- ✅ Workflow triggers on pull requests to main branch
- ✅ Successfully generates and posts Terraform plan to PR comments
- ✅ Correctly fails the PR check if `terraform plan` encounters errors
- ✅ Handles plan output truncation for large plans
- ✅ Posts success/failure status in PR comments
- ✅ Uses correct Terraform version (1.6.6)
- ✅ Includes proper permissions for OIDC and PR commenting

### 2. Security Scan Workflow (`test_security_scan_workflow.py`)
Tests for the `.github/workflows/security-scan.yml` workflow:

#### tfsec Configuration
- ✅ Executes `tfsec` with aquasecurity/tfsec-action@v1.0.3
- ✅ Configures `soft_fail: false` to fail on security issues
- ✅ Runs on push to main and pull requests

#### Checkov Configuration
- ✅ Executes `Checkov` with bridgecrewio/checkov-action@v12
- ✅ Scans current directory with `directory: .`
- ✅ Configured for Terraform framework
- ✅ Configures `soft_fail: false` to fail on policy violations
- ✅ Uses CLI output format

### 3. Backend Configuration (`test_backend_config.py`)
Tests for the `backend.tf` Terraform configuration:
- ✅ Correctly specifies an S3 backend for state management
- ✅ Includes DynamoDB table for state locking
- ✅ Enables encryption with `encrypt = true`
- ✅ Validates AWS region format
- ✅ Validates S3 bucket naming conventions
- ✅ Validates state file key path format (.tfstate)
- ✅ Includes documentation comments
- ✅ All required parameters present (bucket, key, region, encrypt, dynamodb_table)

## Setup

### Install Dependencies

```bash
cd tests
pip install -r requirements.txt
```

Or using a virtual environment:

```bash
cd tests
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Test Plan on PR workflow
pytest test_plan_on_pr_workflow.py

# Test Security Scan workflow
pytest test_security_scan_workflow.py

# Test Backend configuration
pytest test_backend_config.py
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run Verbose Mode

```bash
pytest -v
```

### Run Specific Test Classes

```bash
# Test only tfsec configuration
pytest test_security_scan_workflow.py::TestTfsecJob

# Test only Checkov configuration
pytest test_security_scan_workflow.py::TestCheckovJob

# Test backend configuration
pytest test_backend_config.py::TestBackendConfiguration
```

## Test Structure

Each test file follows a consistent pattern:

1. **Fixtures**: Load and parse configuration files (YAML for workflows, HCL for Terraform)
2. **Test Classes**: Group related tests for better organization
3. **Descriptive Test Names**: Each test clearly describes what it validates
4. **Assertions**: Verify specific configuration values and behaviors

## CI/CD Integration

These tests can be integrated into your CI/CD pipeline:

```yaml
name: Unit Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd tests
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## Requirements

- Python 3.8+
- pytest 7.4.3+
- pyyaml 6.0.1+
- hcl2 4.3.2+

## Contributing

When adding new workflows or Terraform configurations:

1. Create corresponding test files in this directory
2. Follow the existing test patterns and naming conventions
3. Ensure all tests pass before submitting PR
4. Update this README with new test coverage information
