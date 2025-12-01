from __future__ import annotations

import re
from typing import Iterable, List, Mapping, Optional

from .models import DatasetSchema, FieldInfo, PhysicalType, RiskLevel, SemanticType

# Typical field name hints
NAME_HINTS = {"fio", "full_name", "fullname", "last_name", "first_name", "surname", "name"}
PASSPORT_HINTS = {"passport", "паспорт", "doc_number"}
INN_HINTS = {"inn", "инн"}
SNILS_HINTS = {"snils", "снилс"}
PHONE_HINTS = {"phone", "msisdn", "телефон"}
ADDRESS_HINTS = {"address", "addr", "адрес"}
EMAIL_HINTS = {"email", "e-mail", "mail"}
ID_HINTS = {"user_id", "client_id", "account_id", "uid", "guid", "login", "cookie", "session"}


PASSPORT_RE = re.compile(r"^(\d{2}\s?\d{2}\s?\d{6})$")
INN_RE = re.compile(r"^\d{10}(\d{2})?$")
SNILS_RE = re.compile(r"^(\d{3}-?\d{3}-?\d{3}\s?\d{2})$")
PHONE_RE = re.compile(r"^(\+7|8)?[\s\-\(\)]?\d{3}[\s\-\)]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _infer_physical(value: object) -> PhysicalType:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    return "string"


def _any_match(values: List[str], pattern: re.Pattern[str]) -> bool:
    return any(pattern.match(v) for v in values if isinstance(v, str))


def _name_matches(name: str, hints: set[str]) -> bool:
    cleaned = name.lower()
    return any(hint in cleaned for hint in hints)


def _detect_semantic(name: str, values: List[object]) -> Optional[SemanticType]:
    str_values = [str(v).strip() for v in values if v is not None]

    has_passport_hint = _name_matches(name, PASSPORT_HINTS)
    has_inn_hint = _name_matches(name, INN_HINTS)
    has_snils_hint = _name_matches(name, SNILS_HINTS)

    # Prefer format-based detection to avoid misclassifying fields when names are ambiguous
    if _any_match(str_values, INN_RE):
        return SemanticType.INN
    if _any_match(str_values, PASSPORT_RE):
        return SemanticType.PASSPORT
    if _any_match(str_values, SNILS_RE):
        return SemanticType.SNILS

    # When only column hints are available, rely on them as a fallback
    if has_inn_hint:
        return SemanticType.INN if not str_values else None
    if has_passport_hint:
        return SemanticType.PASSPORT if not str_values else None
    if has_snils_hint:
        return SemanticType.SNILS if not str_values else None
    if _name_matches(name, PHONE_HINTS) or _any_match(str_values, PHONE_RE):
        return SemanticType.PHONE
    if _name_matches(name, EMAIL_HINTS) or _any_match(str_values, EMAIL_RE):
        return SemanticType.EMAIL
    if _name_matches(name, ADDRESS_HINTS):
        return SemanticType.ADDRESS
    if _name_matches(name, NAME_HINTS):
        return SemanticType.FIO
    if _name_matches(name, ID_HINTS):
        return SemanticType.CUSTOM_ID
    return None


def _define_risk(semantic: Optional[SemanticType]) -> RiskLevel:
    if semantic in {SemanticType.PASSPORT, SemanticType.INN, SemanticType.SNILS, SemanticType.FIO}:
        return "high"
    if semantic in {
        SemanticType.PHONE,
        SemanticType.EMAIL,
        SemanticType.ADDRESS,
        SemanticType.CUSTOM_ID,
    }:
        return "medium"
    return "low"


def detect_fields(
    columns: Iterable[str], sample_rows: Optional[List[Mapping[str, object]]] = None
) -> DatasetSchema:
    schema = DatasetSchema()
    col_list = list(columns)
    samples = sample_rows or []

    for col in col_list:
        values = [row.get(col) for row in samples if isinstance(row, Mapping)]
        semantic = _detect_semantic(col, values)
        physical: PhysicalType = "string"
        if values:
            for v in values:
                if v is not None:
                    physical = _infer_physical(v)
                    break

        is_pd = semantic not in (None, SemanticType.NON_PD, SemanticType.UNKNOWN)
        field = FieldInfo(
            name=col,
            physical_type=physical,
            semantic_type=semantic or SemanticType.UNKNOWN,
            is_personal_data=is_pd,
            is_sensitive=False,
            risk_level=_define_risk(semantic),
        )
        schema.fields.append(field)
    return schema
