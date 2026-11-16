# Terraform AWS Advanced Orchestration


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![Repo Size](https://img.shields.io/github/repo-size/christophergaughan/terraform-aws-advanced-orchestration)

[![Terraform Validate](https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/validate.yml/badge.svg)](https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/validate.yml)


> Production-ready AWS orchestration infrastructure with observability, CI/CD, and modular Terraform modules.

## CI/CD Status


| Workflow | Status |
|----------|--------|
| Terraform Validate (root, monitoring, bootstrap) | <a href="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/validate.yml"><img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/validate.yml/badge.svg" alt="Terraform Validate" /></a> |
| Terraform Lint | <a href="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/lint.yml"><img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/lint.yml/badge.svg" alt="Terraform Lint" /></a> |
| Security Scan (tfsec + Checkov) | <a href="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/security-scan.yml"><img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/security-scan.yml/badge.svg" alt="Security Scan" /></a> |
| Unit Tests | <a href="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/unit-tests.yml"><img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/unit-tests.yml/badge.svg" alt="Unit Tests" /></a> |
| Terraform Plan on PR | _Runs on pull requests; posts each stack's plan as a comment_ |
| Terraform Apply / Destroy | _Manual, approval-gated (see [CI/CD and Operations](#cicd-and-operations))_ |


## Overview

This repository demonstrates advanced event-driven architecture patterns for automating machine learning and data processing workflows on AWS using Infrastructure as Code (IaC) with Terraform.

**Core Components:**
- **EventBridge**: Event-driven workflow triggers (schedules, S3 events, custom events)
- **Lambda**: Serverless compute for data preprocessing and orchestration logic
- **SageMaker**: ML model training, batch inference, and endpoint deployment
- **CloudWatch**: Centralized logging and monitoring with custom metrics

---

## Real-World Use Case: Protein Biomanufacturing ML Pipeline

This architecture was developed to support automated ML workflows for protein chromatography optimization:

| Step | Component | Function |
|------|-----------|----------|
| 1️⃣ | **S3 Trigger** | New experimental chromatography data uploaded |
| 2️⃣ | **Lambda Preprocessor** | Extracts features, validates data quality, formats for ML |
| 3️⃣ | **SageMaker Training** | Retrains hybrid mechanistic-ML model on updated dataset |
| 4️⃣ | **EventBridge Router** | Routes training completion events to monitoring & deployment |
| 5️⃣ | **Model Deployment** | Updated model deployed to inference endpoint for predictions |

**Impact:** Reduced model update cycle from **2 days (manual)** to **2 hours (automated)**.

---

## 🔐 Security & Compliance

Infrastructure security scanning is integrated into CI/CD:

| Tool | Purpose |
|------|---------|
| **Checkov** | Policy-as-code compliance (CIS, SOC2 benchmarks) |
| **tfsec** | Terraform-specific security misconfigurations |

Findings are either fixed or documented with rationale in `.checkov.yml`. K8s manifests are intentionally dev/demo configs with security checks skipped and documented—production deployments would require full hardening.
---

## Architecture

### Event-Driven Pipeline Flow
```
S3 Upload → EventBridge Rule → Lambda Function → SageMaker Job → Model Endpoint
                    ↓
              CloudWatch Logs & Metrics
```

[📄 View Full Architecture Diagram (PDF)](docs/aws_terraform_v2.pdf)

### Module Structure

Modular design for reusability across projects:
```
terraform-aws-advanced-orchestration/
├── data/                    # RNA-seq dataset
├── docker/                  # Container definitions
│   └── feature_engineering/
├── docs/                    # Architecture diagrams
├── k8s/                     # Kubernetes manifests (dev/demo)
├── lambda_function/         # Serverless inference handler
├── modules/                 # Reusable Terraform modules
│   ├── eventbridge/
│   ├── iam_lambda/
│   ├── iam_sagemaker/
│   ├── lambda/
│   ├── sagemaker/
│   └── vpc/
├── monitoring/              # Observability stack
│   └── terraform/
├── notebooks/               # Jupyter analysis
├── tests/                   # pytest suite
├── .checkov.yml             # Security scan config
├── bootstrap/               # One-time setup: state bucket + GitHub OIDC roles
├── backend.tf               # Remote state (S3, native locking)
└── main.tf                  # Root module
```

---

## Observability & Monitoring

### Metrics Tracked
- **Lambda**: Execution time, error rate, memory usage, concurrent executions
- **SageMaker**: Training job duration, model accuracy metrics, endpoint latency
- **EventBridge**: Rule trigger frequency, failed invocations
- **Pipeline**: End-to-end latency from trigger to model deployment

### Monitoring Stack
- **CloudWatch Dashboards**: Real-time pipeline health visualization
- **Grafana Integration**: Custom ML performance metrics
- **Prometheus**: Time-series model drift detection
- **SNS Alerts**: Email/SMS notifications for pipeline failures
- **PagerDuty**: Production incident escalation (optional)

---

## 💰 Cost Optimization

| Service | Pricing | Usage Pattern | Monthly Cost |
|---------|---------|---------------|--------------|
| **Lambda** | $0.20/million requests | ~500 requests/day | ~$3 |
| **EventBridge** | First 14M events free | <100k events/month | $0 |
| **SageMaker** | Spot instances (~70% off) | 10 hrs training/month | $15-50 |
| **S3** | $0.023/GB storage | 100GB data | $2.30 |
| **CloudWatch** | Free tier (10 metrics) | Standard monitoring | $0-5 |

**Estimated Total:** $20-60/month for typical ML workload

**Design Philosophy:** A serverless-first architecture scales to zero when idle, minimizing costs during periods of low activity.

---

## Technical Skills Demonstrated

| Category | Technologies |
|----------|-------------|
| **Infrastructure as Code** | Terraform modules, remote state management, workspaces |
| **CI/CD** | GitHub Actions, automated testing, multi-environment deployment |
| **Event-Driven Architecture** | Decoupled services, asynchronous processing, event routing |
| **MLOps** | Automated model retraining, versioning, A/B deployment strategies |
| **AWS Services** | Lambda, EventBridge, SageMaker, S3, CloudWatch, IAM |
| **Best Practices** | Modular design, version control, comprehensive documentation |
| **Observability** | Metrics collection, alerting, distributed tracing |

---

## Why This Approach?

### Problem
Manual ML workflows are slow, error-prone, and don't scale:
- Scientists manually upload data, trigger training, and deploy models
- No version control for infrastructure
- Difficult to reproduce experiments
- High operational overhead

### Solution
Infrastructure as Code + Event-Driven Architecture:
- ✅ **Automation**: Eliminate manual steps from data → trained model
- ✅ **Reproducibility**: Every deployment is version-controlled and tested
- ✅ **Scalability**: Handle 1 or 1000 experiments with the same infrastructure
- ✅ **Observability**: Full visibility into pipeline health and performance
- ✅ **Collaboration**: Scientists trigger workflows, engineers manage infrastructure

---

## Roadmap

### Phase 1: Core Pipeline (✅ Complete)
- [x] EventBridge → Lambda → SageMaker orchestration
- [x] CI/CD with GitHub Actions
- [x] CloudWatch monitoring
- [x] Modular Terraform design

### Phase 2: Advanced Orchestration (🚧 In Progress)
- [ ] **Step Functions**: Multi-step workflows (DoE → Model → Validation → Deployment loops)
- [ ] **AWS Glue**: Large-scale ETL for chromatography datasets (>100GB)
- [ ] **CloudWatch Alarms**: Automated alerting for model drift and pipeline failures

### Phase 3: Enterprise Features (📋 Planned)
- [ ] **Secrets Manager**: Secure API key handling for LIMS/ELN integration
- [ ] **VPC Configuration**: Network isolation for GxP compliance in biopharma
- [ ] **Multi-Region Deployment**: Disaster recovery and global availability
- [ ] **Cost Allocation Tags**: Detailed cost tracking per project/team

---

## Getting Started

### Prerequisites
- AWS account and AWS CLI signed in with permissions to create IAM roles and S3 buckets
- Terraform >= 1.10 (native S3 state locking)
- GitHub CLI (`gh`) for the one-time repo setup

### First-time setup
State lives in S3 and CI authenticates to AWS with OIDC, so there is a one-time
bootstrap. Follow [`bootstrap/README.md`](bootstrap/README.md).

### Working locally
```bash
git clone https://github.com/christophergaughan/terraform-aws-advanced-orchestration.git
cd terraform-aws-advanced-orchestration

# The state bucket name is kept out of the repo; read it from the bootstrap stack
BUCKET=$(terraform -chdir=bootstrap output -raw state_bucket)

terraform init -backend-config="bucket=${BUCKET}"
terraform plan
```

Validation needs no AWS access at all:
```bash
terraform init -backend=false && terraform validate && terraform test
```

### Configuration
Settings live in `main.tf` and each module's `variables.tf`. The SageMaker
model in `main.tf` uses placeholder values (execution role, image, model
artifact); replace them before applying the root stack.

---

## Use Cases

This architecture pattern applies to:
- **Biomanufacturing**: Automated protein purification optimization
- **Drug Discovery**: High-throughput screening analysis pipelines
- **Genomics**: RNA-seq processing and variant calling workflows
- **Quality Control**: Real-time manufacturing defect detection
- **Research**: Reproducible computational experiments

---

## License & Disclaimer

**Note**: This repository contains reference architecture and starter code for demonstration purposes. While production-ready patterns are used, additional hardening measures (such as security reviews, compliance validation, and load testing) are recommended before deploying in production environments.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request for:
- Bug fixes
- Documentation improvements
- New module implementations
- Architecture enhancements

---

## Contact

**Christopher Gaughan, Ph.D.**  
AI/ML Specialist | Biomanufacturing Infrastructure  
[GitHub](https://github.com/christophergaughan) | [LinkedIn](https://www.linkedin.com/in/gaughanchristopher/)

---

**Built with** ❤️ **for reproducible, scalable ML infrastructure**

---

## CI/CD and Operations

### Pipeline
| Stage | Workflow | AWS access | When |
|-------|----------|------------|------|
| Validate | `validate.yml` → `terraform.yml` (reusable) | None | Every push and PR |
| Format | `lint.yml` | None | Every push and PR |
| Security | `security-scan.yml` (tfsec per stack + Checkov) | None | Push to main and PRs |
| Plan | `plan-on-pr.yml` | Read-only plan role | PRs to main; plan posted as a comment |
| Apply / Destroy | `terraform-apply.yml` | Apply role | Manual; requires approval on the `aws-apply` environment |

Validation includes `terraform test` against a mocked AWS provider, which
catches plan-time errors that `terraform validate` cannot see, with no
credentials and no cost.

### Authentication
GitHub Actions assumes AWS roles through OIDC; the repository stores no AWS
access keys for Terraform. Two roles, split by blast radius:
- **Plan role**: AWS `ReadOnlyAccess` plus read/write on the exact state and
  lock objects. Assumable only from pull requests and from `main`.
- **Apply role**: can change infrastructure. Assumable only by jobs running in
  the `aws-apply` environment, which requires a reviewer's approval. The apply
  workflow shows the plan first and refuses to apply if the plan changed after
  approval.

### State Management
Remote state in a versioned, encrypted, TLS-only S3 bucket with native S3
locking (`use_lockfile`, Terraform >= 1.10), one key per stack. The bucket name
is passed at `terraform init` rather than committed.

### Security Scanning
- **tfsec**: Terraform-specific misconfigurations, run separately on each stack
- **Checkov**: Broad policy-as-code compliance (CIS, SOC2, etc.)

Exceptions are documented next to the code they apply to (`#tfsec:ignore`,
`#checkov:skip`) or in `.checkov.yml`, each with its reason.
