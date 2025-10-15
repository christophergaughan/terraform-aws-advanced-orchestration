# Terraform AWS Advanced Orchestration


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![Repo Size](https://img.shields.io/github/repo-size/christophergaughan/terraform-aws-advanced-orchestration)

![Terraform CI](https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/terraform.yml/badge.svg)


> Production-ready AWS orchestration infrastructure with observability, CI/CD, and modular Terraform modules.

## CI/CD Status


| Workflow | Status |
|----------|--------|
| Terraform Format & Validate | <img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/terraform.yml/badge.svg" alt="Terraform Format & Validate" /> |
| Terraform Lint | <img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/lint.yml/badge.svg" alt="Terraform Lint" /> |
| Deploy Monitoring Stack | <img src="https://github.com/christophergaughan/terraform-aws-advanced-orchestration/actions/workflows/deploy-monitoring.yml/badge.svg" alt="Deploy Monitoring" /> |
| Destroy Monitoring Stack | _Manual Only – Trigger via GitHub UI_ |


## Overview

This repository demonstrates advanced event-driven architecture patterns for automating machine learning and data processing workflows on AWS using Infrastructure as Code (Terraform).

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
├── main.tf                    # Root module orchestration
├── versions.tf                # Terraform & provider versions
├── variables.tf               # Input variables
├── outputs.tf                 # Exported values
├── modules/
│   ├── eventbridge/          # Event routing & rules
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── lambda/               # Serverless compute
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── sagemaker/            # ML training & inference
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── docs/
    └── aws_terraform_v2.pdf   # Architecture diagrams
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

**Design Philosophy:** Serverless-first architecture scales to zero when idle, minimizing costs during low-activity periods.

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
- Scientists manually upload data, trigger training, deploy models
- No version control for infrastructure
- Difficult to reproduce experiments
- High operational overhead

### Solution
Infrastructure as Code + Event-Driven Architecture:
- ✅ **Automation**: Eliminate manual steps from data → trained model
- ✅ **Reproducibility**: Every deployment is version-controlled and tested
- ✅ **Scalability**: Handle 1 or 1000 experiments with same infrastructure
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
- AWS Account with appropriate permissions
- Terraform >= 1.5.0
- AWS CLI configured with credentials

### Quick Deploy
```bash
# Clone repository
git clone https://github.com/christophergaughan/terraform-aws-advanced-orchestration.git
cd terraform-aws-advanced-orchestration

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Deploy infrastructure
terraform apply
```

### Configuration
Customize deployment by editing `variables.tf` or creating a `terraform.tfvars` file:
```hcl
aws_region          = "us-east-1"
project_name        = "my-ml-pipeline"
lambda_memory_mb    = 512
sagemaker_instance  = "ml.m5.large"
```

---

## Use Cases

This architecture pattern is applicable to:
- **Biomanufacturing**: Automated protein purification optimization
- **Drug Discovery**: High-throughput screening analysis pipelines
- **Genomics**: RNA-seq processing and variant calling workflows
- **Quality Control**: Real-time manufacturing defect detection
- **Research**: Reproducible computational experiments

---

## 📄 License & Disclaimer

**Note**: This repository contains reference architecture and starter code for demonstration purposes. While production-ready patterns are used, additional hardening (security reviews, compliance validation, load testing) is recommended before deploying in production environments.

---

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request for:
- Bug fixes
- Documentation improvements
- New module implementations
- Architecture enhancements

---

## 📧 Contact

**Christopher Gaughan, Ph.D.**  
AI/ML Specialist | Biomanufacturing Infrastructure  
[GitHub](https://github.com/christophergaughan) | [LinkedIn](https://www.linkedin.com/in/gaughanchristopher/)

---

**Built with** ❤️ **for reproducible, scalable ML infrastructure**



