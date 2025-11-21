from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from ..dtypes.detectors import detect_fields
from ..policies.model import Policy
from .core import apply_policy_to_dataframe

try:  # pragma: no cover - optional dependency
    from airflow.models import BaseOperator
except Exception:  # pragma: no cover
    class BaseOperator:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise ImportError("Airflow is not installed; use this operator inside Airflow only")


class RuSmbPdAnonymizerOperator(BaseOperator):
    template_fields = ("input_path", "output_path", "policy_path")

    def __init__(
        self,
        *,
        input_path: str,
        output_path: str,
        policy_path: str,
        input_format: str = "csv",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.input_path = input_path
        self.output_path = output_path
        self.input_format = input_format
        self.policy_path = policy_path

    def execute(self, context: Optional[dict] = None) -> str:
        policy = Policy.from_yaml(self.policy_path)
        if self.input_format.lower() == "csv":
            df = pd.read_csv(self.input_path)
            schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
            anonymized = apply_policy_to_dataframe(df, schema, policy)
            anonymized.to_csv(self.output_path, index=False)
        elif self.input_format.lower() in {"parquet", "pq"}:
            df = pd.read_parquet(self.input_path)
            schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
            anonymized = apply_policy_to_dataframe(df, schema, policy)
            anonymized.to_parquet(self.output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {self.input_format}")
        return self.output_path
