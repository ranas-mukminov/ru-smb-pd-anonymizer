from __future__ import annotations

import importlib
from typing import Dict, Iterable, Iterator, List

import pandas as pd

from ..dtypes.models import DatasetSchema, FieldInfo, SemanticType
from ..policies.model import FieldPolicy, Policy


def _resolve_transformer(name: str, params: Dict) -> object:
    if not name:
        raise ValueError("Transformer name is required in policy")
    if "." in name:
        module_name, class_name = name.rsplit(".", 1)
    else:
        module_name, class_name = name, None
    module_path = f"ru_smb_pd_anonymizer.transforms.{module_name}"
    module = importlib.import_module(module_path)
    class_obj = getattr(module, class_name) if class_name else None
    transformer = class_obj(**params) if class_obj else None
    return transformer


def _match_field(field: FieldInfo, fp: FieldPolicy) -> bool:
    pattern = fp.field_pattern
    if pattern.startswith("semantic:"):
        semantic = pattern.split(":", 1)[1]
        return field.semantic_type.value == semantic if field.semantic_type else False
    return pattern in field.name


def _select_policies(schema: DatasetSchema, policy: Policy) -> Dict[str, FieldPolicy]:
    mapping: Dict[str, FieldPolicy] = {}
    for field in schema.fields:
        for fp in policy.fields:
            if _match_field(field, fp):
                mapping[field.name] = fp
                break
    return mapping


def apply_policy_to_dataframe(df: pd.DataFrame, schema: DatasetSchema, policy: Policy) -> pd.DataFrame:
    result = df.copy()
    mapping = _select_policies(schema, policy)

    for col, fp in mapping.items():
        transformer = _resolve_transformer(fp.transformer, fp.params or {}) if fp.transformer else None
        if transformer is None:
            continue
        if hasattr(transformer, "fit"):
            transformer.fit(df[col])
        result[col] = transformer.transform(df[col])
    return result


def apply_policy_stream(records: Iterable[Dict[str, object]], schema: DatasetSchema, policy: Policy) -> Iterator[Dict[str, object]]:
    df = pd.DataFrame(list(records))
    if df.empty:
        return iter([])
    transformed = apply_policy_to_dataframe(df, schema, policy)
    return (row._asdict() if hasattr(row, "_asdict") else row for row in transformed.to_dict(orient="records"))
