# Bootstrap: one-time AWS + GitHub setup

Creates what CI needs before it can touch AWS:

| Resource | Purpose |
|----------|---------|
| S3 bucket `tf-advanced-orchestration-state-<random>` | Terraform state for the root and monitoring stacks. Versioned, KMS-encrypted, TLS-only, public access blocked, old versions expire after 90 days. Locking uses S3 lock files (no DynamoDB). |
| GitHub OIDC provider | Lets GitHub Actions get short-lived AWS credentials. No access keys stored in GitHub. |
| `gha-terraform-plan` role | `ReadOnlyAccess` + read/write on the exact state and lock objects. Assumable only from pull requests and from `main`. |
| `gha-terraform-apply` role | Can change infrastructure. Assumable only by jobs in the `aws-apply` GitHub environment, which requires your approval. |

Cost: the bucket holds a few KB of state (cents per month). IAM and OIDC are free.

Every command below is a plain shell command. Run them in Warp (or any terminal)
on your Mac, from the repository folder.

---

## 0. Check your tools

```bash
terraform version              # needs 1.10 or newer
aws sts get-caller-identity    # prints your account: you're signed in to AWS
gh auth status                 # GitHub CLI signed in
```

If something is missing:

```bash
brew install hashicorp/tap/terraform    # or: brew upgrade hashicorp/tap/terraform
brew install gh && gh auth login
```

## 1. Apply the patch

```bash
cd ~/path/to/terraform-aws-advanced-orchestration
git switch main && git pull
git status                     # should say "working tree clean"
git apply --check ~/Downloads/terraform-ci-overhaul.patch && git apply ~/Downloads/terraform-ci-overhaul.patch
```

## 2. Does your account already have a GitHub OIDC provider?

An AWS account can only have one per URL.

```bash
aws iam list-open-id-connect-providers
```

If any ARN ends in `token.actions.githubusercontent.com`, add
`-var create_oidc_provider=false` to the `terraform plan` command in step 3.

## 3. Create the bootstrap resources

```bash
cd bootstrap
terraform init
terraform plan -out=bootstrap.tfplan      # expect 16 to add (15 with create_oidc_provider=false)
terraform apply bootstrap.tfplan
```

This stack keeps its own state locally in `bootstrap/terraform.tfstate`
(gitignored). Keep a copy in the new bucket so it survives a lost laptop:

```bash
aws s3 cp terraform.tfstate "s3://$(terraform output -raw state_bucket)/bootstrap/terraform.tfstate"
```

## 4. Connect GitHub

```bash
./configure-github.sh
```

This sets the `TF_STATE_BUCKET` variable, the `AWS_PLAN_ROLE_ARN` and
`AWS_APPLY_ROLE_ARN` secrets, and creates the `aws-apply` environment with you
as required reviewer (deployable from `main` only). It finishes by checking that
the approval gate is in place.

## 5. Move any existing local state into S3

```bash
cd ..
ls terraform.tfstate monitoring/terraform/terraform.tfstate 2>/dev/null
```

- **Nothing listed:** skip this step.
- **`terraform.tfstate` listed** (root stack):
  ```bash
  terraform init -migrate-state -backend-config="bucket=$(terraform -chdir=bootstrap output -raw state_bucket)"
  ```
- **`monitoring/terraform/terraform.tfstate` listed:**
  ```bash
  cd monitoring/terraform
  terraform init -migrate-state -backend-config="bucket=$(terraform -chdir=../../bootstrap output -raw state_bucket)"
  cd ../..
  ```

Answer `yes` when Terraform asks to copy the state.

If you created resources in the past but no state file exists, Terraform does
not know about them. Check the AWS console (us-east-2) for leftovers such as an
`orchestration-metrics` Prometheus workspace or `grafana-admin-role`, and delete
or `terraform import` them before applying.

## 6. Commit and push

```bash
git add -A
git status          # confirm no terraform.tfstate or *.tfplan files are staged
git commit -m "CI: OIDC + S3 remote state, approval-gated apply; fix false-green checks"
git push
```

In the Actions tab, expect green runs of **Terraform Validate**,
**Terraform Lint**, **Security Scan** (now three tfsec jobs plus Checkov), and
**Unit Tests**.

## 7. Try a pull-request plan

```bash
git switch -c try-plan
echo "" >> monitoring/terraform/README.md
git commit -am "Test PR plan"
git push -u origin try-plan
gh pr create --fill
```

You should get two PR comments, one per stack, with the account ID redacted.
Then clean up:

```bash
gh pr close try-plan --delete-branch
git switch main
```

## 8. Optional: deploy the monitoring stack

Grafana uses IAM Identity Center (`AWS_SSO`), which must be enabled in the
account first.

1. Actions → **Terraform Apply / Destroy** → **Run workflow** → branch `main`,
   stack `monitoring`, action `apply`.
2. Open the run and read the plan in the **plan** job's summary.
3. Click **Review deployments** → approve `aws-apply`.
4. The apply job re-plans, refuses if anything changed since your approval, then applies.

Tear it down the same way with action `destroy`.

## 9. Retire the old access keys (when ready)

The Terraform workflows no longer use `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY`, but `run-pca.yml` and `run-preprocessing.yml` still do.
Once those are migrated or retired:

```bash
gh secret delete AWS_ACCESS_KEY_ID
gh secret delete AWS_SECRET_ACCESS_KEY
```

Then deactivate that IAM user's access key in the AWS console.

---

## Troubleshooting

| Error | Cause and fix |
|-------|---------------|
| `EntityAlreadyExists: Provider with url https://token.actions.githubusercontent.com already exists` | The account already has the OIDC provider. Re-run step 3 with `-var create_oidc_provider=false`. |
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | The run's identity doesn't match the trust policy. Plans must run from a PR in this repo or from `main`; apply must run in the `aws-apply` environment. |
| `Environment 'aws-apply' is missing or has no required reviewer` | Run `./configure-github.sh` (step 4). |
| `Error acquiring the state lock` | Another plan or apply holds the lock. Wait for it. If a run was killed mid-plan, `terraform force-unlock <LOCK_ID>` from your machine. |
| `Plan changed since approval` | Something changed between the reviewed plan and the apply. Re-run the workflow and review again. |

## Removing everything later

Destroy the monitoring (and root) stacks through the workflow first. Then, in
`bootstrap/state.tf`, delete the `prevent_destroy` lifecycle block, empty the
bucket (including old versions), and run `terraform destroy` here.
