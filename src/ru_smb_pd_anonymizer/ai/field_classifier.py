from __future__ import annotations

from typing import Dict, Iterable, Optional

from ..dtypes.detectors import detect_fields
from ..dtypes.models import DatasetSchema
from .base import AIProvider, NoopAIProvider


def suggest_semantics(
    columns: Iterable[str],
    samples: Optional[list[dict]] = None,
    provider: Optional[AIProvider] = None,
    allow_external: bool = False,
) -> DatasetSchema:
    """Suggest semantic types for fields.

    By default uses local heuristics; if allow_external=True and provider is not Noop,
    caller is responsible for ensuring no raw PII is sent.
    """

    schema = detect_fields(columns, samples)

    if not allow_external or provider is None or isinstance(provider, NoopAIProvider):
        return schema

    descriptions = {c: "" for c in columns}
    prompt = "Suggest semantic types for columns: " + ", ".join(columns)
    _ = provider.complete(prompt)  # External call is under caller control
    return schema
