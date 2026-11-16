#!/usr/bin/env bash
# Wires the bootstrap outputs into GitHub:
#   - repo variable  TF_STATE_BUCKET
#   - repo secrets   AWS_PLAN_ROLE_ARN, AWS_APPLY_ROLE_ARN
#   - environment    aws-apply, with you as required reviewer, main branch only
#
# Run from anywhere AFTER `terraform apply` in bootstrap/. Needs the GitHub
# CLI, signed in (`gh auth login`). Safe to re-run.
set -euo pipefail

REPO="${REPO:-christophergaughan/terraform-aws-advanced-orchestration}"
ENVIRONMENT="aws-apply"

command -v gh >/dev/null || { echo "GitHub CLI not found. Install it: brew install gh"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "GitHub CLI is not signed in. Run: gh auth login"; exit 1; }

cd "$(dirname "$0")"
bucket=$(terraform output -raw state_bucket)
plan_role=$(terraform output -raw plan_role_arn)
apply_role=$(terraform output -raw apply_role_arn)

echo "-> Repo variable TF_STATE_BUCKET"
gh variable set TF_STATE_BUCKET --repo "$REPO" --body "$bucket"

echo "-> Repo secrets AWS_PLAN_ROLE_ARN and AWS_APPLY_ROLE_ARN"
gh secret set AWS_PLAN_ROLE_ARN --repo "$REPO" --body "$plan_role"
gh secret set AWS_APPLY_ROLE_ARN --repo "$REPO" --body "$apply_role"

echo "-> Environment '$ENVIRONMENT': you as required reviewer, deployable from main only"
user_id=$(gh api user --jq .id)
gh api --method PUT "repos/$REPO/environments/$ENVIRONMENT" --input - >/dev/null <<JSON
{
  "reviewers": [{ "type": "User", "id": $user_id }],
  "deployment_branch_policy": { "protected_branches": false, "custom_branch_policies": true }
}
JSON

if ! gh api "repos/$REPO/environments/$ENVIRONMENT/deployment-branch-policies" \
      --jq '.branch_policies[].name' | grep -qx main; then
  gh api --method POST "repos/$REPO/environments/$ENVIRONMENT/deployment-branch-policies" \
    -f name=main -f type=branch >/dev/null
fi

echo "-> Verifying"
reviewers=$(gh api "repos/$REPO/environments/$ENVIRONMENT" \
  --jq '[.protection_rules[] | select(.type == "required_reviewers")] | length')
if [ "$reviewers" -lt 1 ]; then
  echo "ERROR: '$ENVIRONMENT' has no required reviewer. Set one in Settings > Environments." >&2
  exit 1
fi
gh variable list --repo "$REPO" | grep -q '^TF_STATE_BUCKET' && echo "   TF_STATE_BUCKET set"
gh secret list --repo "$REPO" | grep -E '^AWS_(PLAN|APPLY)_ROLE_ARN' | awk '{print "   " $1 " set"}'
echo "   $ENVIRONMENT requires approval"
echo "Done."
