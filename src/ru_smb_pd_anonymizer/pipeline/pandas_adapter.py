from __future__ import annotations

import pandas as pd

from ..dtypes.detectors import detect_fields
from ..policies.model import Policy
from .core import apply_policy_to_dataframe


def anonymize_csv(input_path: str, output_path: str, policy: Policy) -> None:
    df = pd.read_csv(input_path)
    schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
    anonymized = apply_policy_to_dataframe(df, schema, policy)
    anonymized.to_csv(output_path, index=False)


def anonymize_parquet(input_path: str, output_path: str, policy: Policy) -> None:
    df = pd.read_parquet(input_path)
    schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
    anonymized = apply_policy_to_dataframe(df, schema, policy)
    anonymized.to_parquet(output_path, index=False)
