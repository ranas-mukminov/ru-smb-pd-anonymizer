from __future__ import annotations

from typing import Dict

import pandas as pd

from ..dtypes.models import DatasetSchema, RiskLevel, SemanticType


RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


def score_field(series: pd.Series, semantic_type: SemanticType) -> RiskLevel:
    unique_count = series.nunique(dropna=True)
    total = max(len(series), 1)
    uniqueness_ratio = unique_count / total

    if semantic_type in {SemanticType.PASSPORT, SemanticType.SNILS, SemanticType.INN}:
        return "high"
    if semantic_type in {SemanticType.FIO, SemanticType.PHONE, SemanticType.EMAIL}:
        return "medium" if uniqueness_ratio < 0.5 else "high"
    if uniqueness_ratio < 0.1:
        return "high"
    if uniqueness_ratio < 0.5:
        return "medium"
    return "low"


def score_dataset(df: pd.DataFrame, schema: DatasetSchema) -> Dict[str, RiskLevel]:
    scores: Dict[str, RiskLevel] = {}
    for field in schema.fields:
        if field.name not in df:
            continue
        series = df[field.name]
        scores[field.name] = score_field(series, field.semantic_type or SemanticType.UNKNOWN)
    return scores
