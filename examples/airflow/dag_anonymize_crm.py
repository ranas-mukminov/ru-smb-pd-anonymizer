"""Пример DAG для анонимизации CRM-выгрузки."""
from __future__ import annotations

from datetime import datetime

try:  # pragma: no cover - optional dependency
    from airflow import DAG
except Exception:  # pragma: no cover
    DAG = None

from ru_smb_pd_anonymizer.pipeline.airflow_operator import RuSmbPdAnonymizerOperator

if DAG:
    with DAG(
        dag_id="anonymize_crm",
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,
        catchup=False,
        default_args={"owner": "data"},
    ) as dag:
        anonymize = RuSmbPdAnonymizerOperator(
            task_id="anonymize_crm_csv",
            input_path="/opt/airflow/data/crm.csv",
            output_path="/opt/airflow/data/crm_anon.csv",
            policy_path="/opt/airflow/dags/policy_analytics.yaml",
            input_format="csv",
        )
else:  # pragma: no cover
    anonymize = None
