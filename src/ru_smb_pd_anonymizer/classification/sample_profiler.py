from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class FieldProfile:
    unique_count: int
    null_fraction: float
    sample_values: list


@dataclass
class DatasetProfile:
    fields: Dict[str, FieldProfile]


def profile_dataframe(df: pd.DataFrame, sample_size: int = 5) -> DatasetProfile:
    profiles: Dict[str, FieldProfile] = {}
    for col in df.columns:
        series = df[col]
        unique_count = series.nunique(dropna=True)
        null_fraction = float(series.isna().mean())
        samples = series.dropna().astype(str).head(sample_size).tolist()
        profiles[col] = FieldProfile(
            unique_count=unique_count,
            null_fraction=null_fraction,
            sample_values=samples,
        )
    return DatasetProfile(fields=profiles)
