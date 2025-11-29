from __future__ import annotations

from typing import Iterable, Mapping, Optional

from ..dtypes.detectors import detect_fields
from ..dtypes.models import DatasetSchema


def analyze_schema(
    columns: Iterable[str], samples: Optional[list[Mapping[str, object]]] = None
) -> DatasetSchema:
    return detect_fields(columns, samples)
