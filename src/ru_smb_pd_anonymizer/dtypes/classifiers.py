from __future__ import annotations

from typing import Iterable, Mapping, Optional

from .detectors import detect_fields
from .models import DatasetSchema, SemanticType


def classify_schema(
    columns: Iterable[str], sample_rows: Optional[list[Mapping[str, object]]] = None
) -> DatasetSchema:
    """Lightweight wrapper over detect_fields for clarity."""
    return detect_fields(columns, sample_rows)


def is_personal_field(field_name: str, schema: DatasetSchema) -> bool:
    field = schema.get_field(field_name)
    if not field:
        return False
    return field.semantic_type not in {SemanticType.UNKNOWN, SemanticType.NON_PD}
