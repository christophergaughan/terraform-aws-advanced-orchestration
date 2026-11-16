"""Unit tests for the S3 remote-state backend configuration.

Both stacks (root and monitoring) store state in the bucket created by
./bootstrap, under separate keys, with native S3 locking (use_lockfile).
The bucket name is supplied at init time, so it must NOT be hardcoded.
"""

import os
import re

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

BACKENDS = {
    "root": ("backend.tf", "advanced-orchestration/root.tfstate"),
    "monitoring": ("monitoring/terraform/backend.tf", "advanced-orchestration/monitoring.tfstate"),
}

BOOTSTRAP_LOCALS = os.path.join(REPO_ROOT, "bootstrap", "oidc.tf")


def _strip_comments(text):
    """Drop full-line and trailing # / // comments so checks see live config only."""
    return "\n".join(re.split(r"\s(#|//)|^(#|//)", line)[0] for line in text.splitlines())


@pytest.fixture(params=sorted(BACKENDS), ids=sorted(BACKENDS))
def backend(request):
    rel_path, expected_key = BACKENDS[request.param]
    path = os.path.join(REPO_ROOT, rel_path)
    with open(path, "r") as f:
        raw = f.read()
    return {"path": path, "raw": raw, "live": _strip_comments(raw), "expected_key": expected_key}


class TestBackendConfiguration:
    """Every stack uses the S3 backend, uncommented and correctly keyed."""

    def test_backend_file_exists(self, backend):
        assert os.path.isfile(backend["path"])

    def test_s3_backend_is_active_not_commented(self, backend):
        assert re.search(r'backend\s+"s3"\s*\{', backend["live"]), \
            "S3 backend block must be live config, not a comment"

    def test_key_is_stack_specific(self, backend):
        match = re.search(r'key\s*=\s*"([^"]+)"', backend["live"])
        assert match, "backend must set key"
        assert match.group(1) == backend["expected_key"]

    def test_region_is_valid_aws_region(self, backend):
        match = re.search(r'region\s*=\s*"([^"]+)"', backend["live"])
        assert match, "backend must set region"
        assert re.match(r"^[a-z]{2}-[a-z]+-\d$", match.group(1))

    def test_encryption_enabled(self, backend):
        assert re.search(r"encrypt\s*=\s*true", backend["live"])

    def test_native_s3_locking_enabled(self, backend):
        assert re.search(r"use_lockfile\s*=\s*true", backend["live"]), \
            "use S3 lock files (Terraform >= 1.10)"

    def test_no_deprecated_dynamodb_locking(self, backend):
        assert "dynamodb_table" not in backend["live"], \
            "DynamoDB locking is deprecated; use_lockfile replaces it"

    def test_bucket_not_hardcoded(self, backend):
        assert not re.search(r"\bbucket\s*=", backend["live"]), \
            "bucket is supplied via -backend-config so it stays out of the public repo"

    def test_documents_how_to_supply_bucket(self, backend):
        assert "-backend-config" in backend["raw"]


class TestBackendMatchesBootstrap:
    """The bootstrap roles grant access to exactly the keys the backends use."""

    def test_bootstrap_grants_each_backend_key(self):
        with open(BOOTSTRAP_LOCALS, "r") as f:
            bootstrap = f.read()
        for _, key in BACKENDS.values():
            assert f'"{key}"' in bootstrap, f"bootstrap state_keys is missing {key}"

    def test_backends_share_region_with_bootstrap_default(self):
        with open(os.path.join(REPO_ROOT, "bootstrap", "variables.tf"), "r") as f:
            variables = f.read()
        default_region = re.search(
            r'variable "region"\s*\{[^}]*default\s*=\s*"([^"]+)"', variables, re.S
        ).group(1)
        for rel_path, _ in BACKENDS.values():
            with open(os.path.join(REPO_ROOT, rel_path), "r") as f:
                region = re.search(r'region\s*=\s*"([^"]+)"', _strip_comments(f.read())).group(1)
            assert region == default_region, f"{rel_path} region must match the state bucket region"
