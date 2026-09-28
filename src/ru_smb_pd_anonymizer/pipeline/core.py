from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Literal, Protocol, Tuple, cast, overload

import pandas as pd

from ..dtypes.models import DatasetSchema, FieldInfo
from ..policies.model import FieldPolicy, Policy


@dataclass
class PolicyApplicationReport:
    """Short report about how a policy was applied to a DataFrame."""

    policy_name: str
    rows_processed: int
    columns_anonymized: Dict[str, str]
    columns_skipped: List[str]


class _Transformer(Protocol):
    def transform(self, series: pd.Series) -> pd.Series: ...


def _resolve_transformer(name: str, params: Dict) -> _Transformer | None:
    if not name:
        raise ValueError("Transformer name is required in policy")

    module_name: str
    class_name: str | None

    if "." in name:
        module_name, class_name = name.rsplit(".", 1)
        if module_name.startswith("ru_smb_pd_anonymizer.transforms"):
            module_path = module_name
        else:
            module_path = f"ru_smb_pd_anonymizer.transforms.{module_name}"
    else:
        module_path, class_name = f"ru_smb_pd_anonymizer.transforms.{name}", None

    module = importlib.import_module(module_path)
    class_obj = getattr(module, class_name) if class_name else None
    transformer = class_obj(**params) if class_obj else None
    return cast(_Transformer | None, transformer)


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


@overload
def apply_policy_to_dataframe(
    df: pd.DataFrame,
    schema: DatasetSchema,
    policy: Policy,
    return_report: Literal[False] = False,
) -> pd.DataFrame: ...


@overload
def apply_policy_to_dataframe(
    df: pd.DataFrame,
    schema: DatasetSchema,
    policy: Policy,
    return_report: Literal[True],
) -> Tuple[pd.DataFrame, PolicyApplicationReport]: ...


def apply_policy_to_dataframe(
    df: pd.DataFrame,
    schema: DatasetSchema,
    policy: Policy,
    return_report: bool = False,
) -> pd.DataFrame | Tuple[pd.DataFrame, PolicyApplicationReport]:
    result = df.copy()
    mapping = _select_policies(schema, policy)

    applied: Dict[str, str] = {}
    skipped: set[str] = set()

    for col, fp in mapping.items():
        transformer = (
            _resolve_transformer(fp.transformer, fp.params or {}) if fp.transformer else None
        )
        if transformer is None:
            skipped.add(col)
            continue
        fit = getattr(transformer, "fit", None)
        if callable(fit):
            fit(df[col])
        result[col] = transformer.transform(df[col])
        applied[col] = fp.transformer or transformer.__class__.__name__

    if return_report:
        # mark columns from schema that were not matched by any policy
        skipped.update({field.name for field in schema.fields if field.name not in mapping})

        report = PolicyApplicationReport(
            policy_name=policy.name,
            rows_processed=len(df),
            columns_anonymized=applied,
            columns_skipped=sorted(skipped),
        )
        return result, report
    return result


def apply_policy_stream(
    records: Iterable[Dict[str, object]],
    schema: DatasetSchema,
    policy: Policy,
) -> Iterator[Dict[str, object]]:
    df = pd.DataFrame(list(records))
    if df.empty:
        return iter([])
    transformed = apply_policy_to_dataframe(df, schema, policy)
    return (
        row._asdict() if hasattr(row, "_asdict") else row
        for row in transformed.to_dict(orient="records")
    )
