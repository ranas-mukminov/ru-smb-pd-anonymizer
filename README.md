# ru-smb-pd-anonymizer 🔒

[![CI](https://github.com/ranas-mukminov/ru-smb-pd-anonymizer/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/ru-smb-pd-anonymizer/actions/workflows/ci.yml)
[![Security](https://github.com/ranas-mukminov/ru-smb-pd-anonymizer/actions/workflows/security.yml/badge.svg)](https://github.com/ranas-mukminov/ru-smb-pd-anonymizer/actions/workflows/security.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

---

## Overview

**ru-smb-pd-anonymizer** is a production-ready Python framework for anonymizing and pseudonymizing Russian personal data before sharing datasets with AI/LLM services, outsourcing teams, analytics departments, or technical support. Designed specifically for small and medium businesses in Russia, this toolkit provides compliance-aware data masking, tokenization, and transformation capabilities tailored to Russian data protection legislation (Federal Law 152-ФЗ).

The framework includes detectors for Russian-specific identifiers (FIO, passport numbers, INN, SNILS, phone numbers, addresses, emails), reusable transformers for various anonymization strategies, pre-built policies for common use cases, and pipeline adapters for popular data processing tools like pandas, SQLAlchemy, Apache Airflow, and dbt. An optional AI layer helps suggest anonymization policies based on schema analysis, without sending raw personal data externally by default.

This is a technical toolkit: legal assessment of anonymization adequacy remains the responsibility of your legal counsel or compliance team.

---

## Key Features

- **Russian PD detectors** – Automatic identification of FIO (full name), passport, INN, SNILS, phone numbers, postal addresses, and emails using regex patterns and heuristics
- **Flexible transformation strategies** – Masking, tokenization, hashing with salt, generalization, noise injection, and hooks for Format-Preserving Encryption (FPE)
- **Pre-built policies** – Ready-to-use anonymization policies for analytics, ML training, technical support, and log processing
- **Multi-format support** – Process CSV files, pandas DataFrames, SQLAlchemy queries, and integrate with Airflow DAGs or dbt macros
- **CLI and Python API** – Command-line interface for quick tasks and programmatic API for integration into existing pipelines
- **AI-assisted policy suggestions** – Optional schema analysis and policy recommendations without exposing real personal data
- **Built for compliance** – Designed with Russian data protection requirements in mind, supporting both irreversible anonymization and reversible pseudonymization
- **Production-grade tooling** – Type-safe code with mypy, comprehensive tests, CI/CD workflows, security scanning with bandit and pip-audit
- **Open source** – Apache 2.0 license for commercial and non-commercial use

---

## Architecture / Components

The framework consists of several modular components that work together:

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI / Python API                        │
│        (ru-pd-anon commands, Python library imports)         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   v
┌─────────────────────────────────────────────────────────────┐
│                   Pipeline Adapters                          │
│  • pandas adapter (CSV, DataFrames)                          │
│  • SQLAlchemy adapter (database queries)                     │
│  • Airflow operator (DAG tasks)                              │
│  • dbt macros (SQL transformations)                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   v
┌─────────────────────────────────────────────────────────────┐
│              Policy Engine + Classification                  │
│  • Field detection (semantic types: FIO, Phone, etc.)        │
│  • Risk assessment (sensitivity levels)                      │
│  • Policy matching (YAML-based rules)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   v
┌─────────────────────────────────────────────────────────────┐
│                   Transformers Layer                         │
│  • FIO masking/tokenization                                  │
│  • Passport masking                                          │
│  • Phone/email tokenization                                  │
│  • INN/SNILS hashing                                         │
│  • Generic ID transformers                                   │
│  • Address generalization                                    │
└─────────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Raw data enters via CLI, Python API, or pipeline adapter (pandas, SQLAlchemy, Airflow, dbt)
2. Schema is analyzed and fields are classified by semantic type
3. Policy engine applies matching rules based on field types and sensitivity levels
4. Transformers apply anonymization/pseudonymization to matching fields
5. Anonymized data is written to output destination

---

## Requirements

### System Requirements

- **Operating System:** Linux (Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+), macOS 11+, or Windows 10+ with WSL2
- **Python:** 3.10 or higher
- **CPU/Memory:** Minimal – 1 CPU core, 512 MB RAM for basic usage; 2+ cores and 2+ GB RAM recommended for large datasets
- **Disk Space:** ~100 MB for package and dependencies

### Python Dependencies

Core dependencies (automatically installed):
- `pandas>=1.5` – DataFrame processing
- `pydantic>=2.6` – Schema validation and type safety
- `PyYAML>=6.0` – Policy file parsing
- `typer>=0.9` – CLI interface
- `sqlalchemy>=1.4` – Database query support
- `rich>=13.0` – Terminal output formatting

### Optional Dependencies

For development and testing:
```bash
pip install ru-smb-pd-anonymizer[dev,test]
```

For Apache Airflow integration:
- `apache-airflow>=2.5` (not bundled, install separately)

For dbt integration:
- `dbt-core>=1.5` (not bundled, install separately)

### Access Requirements

- **Python package installation:** Internet access to PyPI or local mirror
- **File system:** Read/write access to input/output data directories
- **Database access:** Appropriate credentials if using SQLAlchemy adapter

---

## Quick Start (TL;DR)

Get started in under 5 minutes:

**1. Install the package**
```bash
pip install ru-smb-pd-anonymizer
```

**2. Inspect your data schema**
```bash
ru-pd-anon inspect-schema \
  --input examples/data/synthetic_crm.csv \
  --format csv \
  --out schema.json
```

**3. Generate an anonymization policy**
```bash
ru-pd-anon suggest-policy \
  --schema schema.json \
  --use-case analytics \
  --out policy.yaml
```

**4. Apply the policy to anonymize your data**
```bash
ru-pd-anon apply-policy \
  --input examples/data/synthetic_crm.csv \
  --format csv \
  --schema schema.json \
  --policy policy.yaml \
  --output examples/data/synthetic_crm_anon.csv
```

Need a quick win for stakeholders? Add `--report` to show how many rows were processed and which columns were anonymized:

```bash
ru-pd-anon apply-policy \
  --input examples/data/synthetic_crm.csv \
  --format csv \
  --schema schema.json \
  --policy policy.yaml \
  --output examples/data/synthetic_crm_anon.csv \
  --report
```

**5. Verify the results**
```bash
head examples/data/synthetic_crm_anon.csv
```

You should see masked FIO, tokenized phone numbers and emails, and hashed identifiers while preserving the data structure for analytics.

---

## Detailed Installation

### Install from PyPI (Recommended)

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or on Windows: venv\Scripts\activate

# Install the package
pip install ru-smb-pd-anonymizer

# Verify installation
ru-pd-anon --version
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/ranas-mukminov/ru-smb-pd-anonymizer.git
cd ru-smb-pd-anonymizer

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode with dev dependencies
pip install -e .[dev,test]

# Run tests to verify installation
pytest

# Run linter and type checker
scripts/lint.sh
```

### Install with Docker (Optional)

```bash
# Clone the repository
git clone https://github.com/ranas-mukminov/ru-smb-pd-anonymizer.git
cd ru-smb-pd-anonymizer

# Build Docker image
docker build -t ru-smb-pd-anonymizer:latest .

# Run anonymization in container
docker run --rm \
  -v $(pwd)/examples/data:/data \
  ru-smb-pd-anonymizer:latest \
  ru-pd-anon apply-policy \
    --input /data/synthetic_crm.csv \
    --format csv \
    --policy /data/policy_analytics.yaml \
    --output /data/synthetic_crm_anon.csv
```

---

## Configuration

### Policy Files

Anonymization policies are defined in YAML format. A policy specifies:
- Field matching patterns (by name or semantic type)
- Anonymization level (irreversible, one-way pseudonymization, reversible pseudonymization)
- Transformer to apply
- Optional parameters for the transformer

**Example policy for analytics:**

```yaml
# examples/configs/policy_analytics.yaml
name: example_analytics
use_case: analytics
description: "Analytics use case with aggressive anonymization"

fields:
  # Full names: irreversible masking
  - field_pattern: "semantic:FIO"
    level: ANONYMIZED_IRREVERSIBLE
    transformer: fio.FioMaskingTransformer
  
  # Passport numbers: partial masking
  - field_pattern: "semantic:Passport"
    level: PSEUDONYMIZED_ONE_WAY
    transformer: passport.PassportMaskingTransformer
    params:
      keep: 2  # Keep first 2 digits
  
  # Phone numbers: tokenization (reversible with key)
  - field_pattern: "semantic:Phone"
    level: PSEUDONYMIZED_REVERSIBLE
    transformer: phone.PhoneTokenizationTransformer
  
  # Emails: tokenization
  - field_pattern: "semantic:Email"
    level: PSEUDONYMIZED_REVERSIBLE
    transformer: email.EmailTokenizationTransformer
  
  # Internal IDs: one-way hashing
  - field_pattern: "semantic:CustomID"
    level: PSEUDONYMIZED_ONE_WAY
    transformer: generic_id.GenericIdHashingTransformer

global_rules:
  require_irreversible_for_sensitive: true
```

**Example policy for ML training:**

```yaml
# examples/configs/policy_ml_training.yaml
name: ml_training
use_case: ml
description: "ML training with balanced privacy and utility"

fields:
  - field_pattern: "semantic:FIO"
    level: ANONYMIZED_IRREVERSIBLE
    transformer: fio.FioGeneralizationTransformer  # Keep first letter
  
  - field_pattern: "semantic:Phone"
    level: PSEUDONYMIZED_ONE_WAY
    transformer: phone.PhoneHashingTransformer  # Consistent hashing
  
  - field_pattern: "semantic:Email"
    level: PSEUDONYMIZED_ONE_WAY
    transformer: email.EmailDomainOnlyTransformer  # Keep domain
  
  - field_pattern: "semantic:INN"
    level: PSEUDONYMIZED_ONE_WAY
    transformer: inn.InnHashingTransformer

global_rules:
  preserve_nulls: true
  preserve_types: true
```

### Environment Variables

Optional configuration via environment variables:

```bash
# Logging level (DEBUG, INFO, WARNING, ERROR)
export RU_PD_ANON_LOG_LEVEL=INFO

# Custom policy directory
export RU_PD_ANON_POLICY_DIR=/etc/ru-pd-anon/policies

# AI service endpoint (if using external AI for policy suggestions)
export RU_PD_ANON_AI_ENDPOINT=http://localhost:8000

# Disable AI features (default: enabled)
export RU_PD_ANON_DISABLE_AI=true

# Custom salt for hashing transformers
export RU_PD_ANON_HASH_SALT=<your-secure-random-salt>
```

### Schema Files

Schema files describe data structure and are auto-generated during `inspect-schema`:

```json
{
  "columns": [
    {
      "name": "customer_id",
      "dtype": "int64",
      "semantic_type": "CustomID",
      "nullable": false
    },
    {
      "name": "full_name",
      "dtype": "string",
      "semantic_type": "FIO",
      "nullable": false
    },
    {
      "name": "phone",
      "dtype": "string",
      "semantic_type": "Phone",
      "nullable": true
    }
  ]
}
```

---

## Usage & Common Tasks

### Command-Line Interface

**Inspect data schema and detect PD fields:**
```bash
ru-pd-anon inspect-schema \
  --input data/customers.csv \
  --format csv \
  --out customers_schema.json
```

**Suggest anonymization policy based on schema:**
```bash
ru-pd-anon suggest-policy \
  --schema customers_schema.json \
  --use-case analytics \
  --out policy_customers.yaml
```

**Apply policy to anonymize data:**
```bash
ru-pd-anon apply-policy \
  --input data/customers.csv \
  --format csv \
  --schema customers_schema.json \
  --policy policy_customers.yaml \
  --output data/customers_anon.csv
```

**Validate policy file syntax:**
```bash
ru-pd-anon validate-policy --policy policy_customers.yaml
```

### Python API

**Anonymize a pandas DataFrame:**

```python
import pandas as pd
from ru_smb_pd_anonymizer.policies.model import Policy
from ru_smb_pd_anonymizer.pipeline.pandas_adapter import anonymize_dataframe

# Load your data
df = pd.read_csv("data/customers.csv")

# Load anonymization policy
policy = Policy.from_yaml("policy_analytics.yaml")

# Anonymize
df_anon = anonymize_dataframe(df, policy)

# Save result
df_anon.to_csv("data/customers_anon.csv", index=False)
```

**Anonymize CSV files directly:**

```python
from ru_smb_pd_anonymizer.policies.model import Policy
from ru_smb_pd_anonymizer.pipeline.pandas_adapter import anonymize_csv

policy = Policy.from_yaml("policy_analytics.yaml")
anonymize_csv("data/customers.csv", "data/customers_anon.csv", policy)
```

**Use with SQLAlchemy:**

```python
from sqlalchemy import create_engine
from ru_smb_pd_anonymizer.policies.model import Policy
from ru_smb_pd_anonymizer.pipeline.sqlalchemy_adapter import anonymize_query

engine = create_engine("postgresql://user:pass@localhost/db")
policy = Policy.from_yaml("policy_analytics.yaml")

query = "SELECT * FROM customers WHERE created_at > '2024-01-01'"
result_df = anonymize_query(engine, query, policy)
```

### Integration with Apache Airflow

**Create an anonymization DAG:**

```python
from datetime import datetime
from airflow import DAG
from ru_smb_pd_anonymizer.pipeline.airflow_operator import RuSmbPdAnonymizerOperator

with DAG(
    dag_id="anonymize_crm_daily",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    anonymize_task = RuSmbPdAnonymizerOperator(
        task_id="anonymize_crm",
        input_path="/data/crm_{{ ds }}.csv",
        output_path="/data/crm_anon_{{ ds }}.csv",
        policy_path="/config/policy_analytics.yaml",
        input_format="csv",
    )
```

### Integration with dbt

**Use anonymization macro in dbt model:**

```sql
-- models/customers_anon.sql
{{
  config(
    materialized='table'
  )
}}

SELECT
  customer_id,
  {{ ru_pd_anon_mask_fio('full_name') }} as full_name,
  {{ ru_pd_anon_tokenize_phone('phone') }} as phone,
  {{ ru_pd_anon_tokenize_email('email') }} as email,
  created_at
FROM {{ ref('customers_raw') }}
```

---

## Update / Upgrade

### Upgrade Package from PyPI

```bash
# Activate your virtual environment
source venv/bin/activate

# Upgrade to the latest version
pip install --upgrade ru-smb-pd-anonymizer

# Verify new version
ru-pd-anon --version
```

### Update from Source

```bash
cd ru-smb-pd-anonymizer
git pull origin main

# Reinstall with latest changes
pip install -e .[dev,test]

# Run tests to verify
pytest
```

### Breaking Changes

When upgrading between major versions, review the [CHANGELOG.md](CHANGELOG.md) for breaking changes:

- **Policy format changes:** Policy YAML schema may change; validate your policies after upgrade: `ru-pd-anon validate-policy --policy your_policy.yaml`
- **Transformer API changes:** Custom transformers may need updates if base classes change
- **CLI argument changes:** Review CLI help after upgrade: `ru-pd-anon --help`

After upgrading, always validate your policies and test on a sample dataset before production use.

---

## Logs, Monitoring, and Troubleshooting

### Logs

**CLI logging:**
```bash
# Enable debug logging
export RU_PD_ANON_LOG_LEVEL=DEBUG
ru-pd-anon apply-policy --input data.csv --policy policy.yaml --output data_anon.csv
```

**Programmatic logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from ru_smb_pd_anonymizer.pipeline.pandas_adapter import anonymize_csv
# Detailed logs will be printed
```

### Common Issues and Solutions

**Problem: `FileNotFoundError: policy.yaml not found`**
```bash
# Solution: Use absolute paths or verify current directory
ru-pd-anon apply-policy --policy $(pwd)/policy_analytics.yaml ...
```

**Problem: `No transformers applied, output identical to input`**
```bash
# Solution: Verify schema detection and policy field patterns
# 1. Inspect schema
ru-pd-anon inspect-schema --input data.csv --format csv --out schema.json
# 2. Check detected semantic types in schema.json
cat schema.json
# 3. Ensure policy field_pattern matches semantic types
```

**Problem: `ImportError: No module named 'ru_smb_pd_anonymizer'`**
```bash
# Solution: Verify installation and virtual environment
pip list | grep ru-smb-pd-anonymizer
# If not listed, reinstall
pip install ru-smb-pd-anonymizer
```

**Problem: `TypeError: expected str, got None`**
- **Cause:** Null values in columns flagged for anonymization
- **Solution:** Set `preserve_nulls: true` in policy global_rules

**Problem: Airflow operator fails with module import errors**
```bash
# Solution: Install package in Airflow environment
# In Airflow docker-compose.yml or Dockerfile:
pip install ru-smb-pd-anonymizer
# Or add to requirements.txt used by Airflow
```

**Problem: `PermissionError` when writing output**
```bash
# Solution: Check write permissions
chmod u+w output_directory/
```

**Problem: Performance degradation on large datasets**
- **Cause:** Processing entire DataFrame in memory
- **Solution:** Use chunked processing or SQLAlchemy adapter for streaming

**Problem: Hash values not consistent across runs**
- **Cause:** Missing or changing salt value
- **Solution:** Set consistent salt via environment variable:
```bash
export RU_PD_ANON_HASH_SALT=<fixed-secure-value>
```

---

## Security Notes

> [!WARNING]
> This toolkit performs technical anonymization/pseudonymization. Legal qualification of whether the output constitutes "personal data" under Russian or international law must be assessed separately by your legal counsel.

### Security Best Practices

1. **Do not log sensitive data:**
   - Avoid printing raw PD to logs or terminal output
   - Never commit files containing real personal data to version control
   - Use synthetic or pre-anonymized examples in tests and documentation

2. **Protect policy files and salts:**
   - Store policy files in secure locations with appropriate file permissions
   - Use strong, random salt values for hashing transformers
   - Rotate salts periodically if using reversible pseudonymization
   - Store salt values in secrets management systems (e.g., HashiCorp Vault, AWS Secrets Manager)

3. **Secure tokenization keys:**
   - If using reversible tokenization, protect encryption keys with the same rigor as personal data itself
   - Use hardware security modules (HSM) or key management services (KMS) for production

4. **Network security:**
   - If using AI policy suggestion features with external services, use HTTPS and verify TLS certificates
   - Consider using local AI models to avoid sending schema information externally

5. **Access control:**
   - Limit access to anonymization processes to authorized personnel only
   - Log anonymization operations for audit trails
   - Implement role-based access control (RBAC) for policy management

6. **Data minimization:**
   - Anonymize only the data you actually need to share
   - Use the most restrictive anonymization level that still meets your use case requirements
   - Prefer irreversible anonymization (masking) over pseudonymization when possible

7. **Review and test:**
   - Manually review anonymized output samples before sharing
   - Test policies on representative datasets
   - Conduct periodic re-identification risk assessments

8. **Compliance:**
   - Ensure anonymization methods align with regulatory requirements (152-ФЗ, 233-ФЗ)
   - Document your anonymization processes and risk assessments
   - Consult with data protection officers (DPO) and legal counsel

> [!CAUTION]
> **Pseudonymization is not anonymization.** Reversible transformations (tokenization, hashing with known salt) still constitute processing of personal data under Russian law. Use irreversible masking or generalization for true anonymization where re-identification must be prevented.

---

## Project Structure

```
ru-smb-pd-anonymizer/
├── src/ru_smb_pd_anonymizer/       # Main package source code
│   ├── ai/                          # AI schema analysis and policy suggestions
│   ├── classification/              # PD field detection and risk assessment
│   ├── cli/                         # Command-line interface
│   ├── dtypes/                      # Data type definitions and schemas
│   ├── io/                          # Input/output adapters (CSV, JSON, database)
│   ├── pipeline/                    # Pipeline adapters (pandas, SQLAlchemy, Airflow, dbt)
│   ├── policies/                    # Policy models and built-in policies
│   └── transforms/                  # Transformers (masking, tokenization, hashing, etc.)
├── examples/                        # Example datasets, policies, and integrations
│   ├── configs/                     # Sample policy YAML files
│   ├── data/                        # Synthetic datasets for testing
│   ├── airflow/                     # Airflow DAG examples
│   ├── dbt/                         # dbt macros and models
│   └── notebooks/                   # Jupyter notebooks with usage examples
├── tests/                           # Unit and integration tests
│   ├── unit/                        # Unit tests for individual components
│   └── integration/                 # End-to-end integration tests
├── scripts/                         # Development and maintenance scripts
│   ├── lint.sh                      # Code linting (ruff, mypy)
│   ├── security_scan.sh             # Security checks (bandit, pip-audit, safety)
│   └── perf_check.sh                # Performance benchmarks
├── pyproject.toml                   # Package metadata and dependencies
├── CHANGELOG.md                     # Version history and changes
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # Apache 2.0 license
├── LEGAL.md                         # Legal disclaimers and compliance notes
└── README.md                        # This file
```

---

## Roadmap / Plans

Future improvements and features:

- [ ] Support for additional Russian PD types (OGRN, KPP, vehicle plates)
- [ ] Differential privacy mechanisms for aggregate analytics
- [ ] Integration with Spark and Dask for large-scale distributed processing
- [ ] Web UI for policy management and visualization
- [ ] Pre-trained ML models for better semantic field detection
- [ ] Support for unstructured data (text documents, emails)
- [ ] Enhanced FPE (Format-Preserving Encryption) implementations
- [ ] Kubernetes operator for batch anonymization jobs
- [ ] Audit log integration (Elasticsearch, Splunk)

See [open issues](https://github.com/ranas-mukminov/ru-smb-pd-anonymizer/issues) for community requests and bug reports.

---

## Contributing

We welcome contributions from the community! To contribute:

1. **Open an issue** describing your use case, proposed feature, or bug report
   - Provide context: data volume, compliance requirements, environment
   - **Never include real personal data** in issues, pull requests, or code examples

2. **Submit a pull request**
   - Keep changes small and focused on a single feature or fix
   - Add unit tests for new transformers or features
   - Update documentation (README, docstrings, CHANGELOG)
   - Run linters and tests before submitting: `scripts/lint.sh && pytest`

3. **Development setup:**
   ```bash
   git clone https://github.com/ranas-mukminov/ru-smb-pd-anonymizer.git
   cd ru-smb-pd-anonymizer
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .[dev,test]
   ```

4. **Code style:**
   - Use type hints for all functions
   - Follow PEP 8 and PEP 257
   - Keep functions small and testable
   - Never log or print raw personal data in tests, debug output, or samples

5. **Testing:**
   - Run tests: `pytest`
   - Check coverage: `pytest --cov=ru_smb_pd_anonymizer`
   - Security scan: `scripts/security_scan.sh`

6. **Legal disclaimer:**
   - This project is a technical toolkit; legal assessment of anonymization adequacy remains with legal counsel
   - All contributors agree to the Apache 2.0 license terms

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This project is licensed under the **Apache License 2.0**.

You are free to use, modify, and distribute this software for commercial and non-commercial purposes, provided you comply with the license terms.

See the [LICENSE](LICENSE) file for full license text.

---

## Author and Commercial Support

**Author:** [Ranas Mukminov](https://github.com/ranas-mukminov)

This project is developed and maintained by a DevOps and DevSecOps engineer specializing in secure data pipelines and compliance automation for Russian businesses.

### Commercial Support

For production-grade implementation, custom anonymization strategies, compliance audits, or ongoing support, commercial services are available:

- **Infrastructure audit and anonymization pipeline design** – Assess your current data flows and design compliant anonymization workflows
- **Integration with existing systems** – Implement anonymization in your Airflow, dbt, Spark, or custom data platforms
- **Compliance consulting** – Navigate Russian data protection requirements (152-ФЗ, 233-ФЗ) with technical safeguards
- **Custom transformer development** – Build domain-specific anonymization transformers for your business needs
- **Training and support** – On-site or remote training for your engineering and data teams

**Contact:** Visit [https://run-as-daemon.ru](https://run-as-daemon.ru) (Russian) or reach out via [GitHub profile](https://github.com/ranas-mukminov).

---

**Disclaimer:** This framework is a technical tool and does not guarantee legal sufficiency of anonymization. The responsibility for lawful processing, storage, cross-border transfer, and localization of personal data remains with the data controller. Always consult qualified legal counsel for compliance assessments.
