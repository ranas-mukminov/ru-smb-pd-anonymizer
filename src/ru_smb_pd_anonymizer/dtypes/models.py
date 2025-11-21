from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Literal, Optional


class SemanticType(str, Enum):
    FIO = "FIO"
    PASSPORT = "Passport"
    INN = "INN"
    SNILS = "SNILS"
    PHONE = "Phone"
    ADDRESS = "Address"
    EMAIL = "Email"
    CUSTOM_ID = "CustomID"
    NON_PD = "NonPD"
    UNKNOWN = "Unknown"


PhysicalType = Literal["string", "int", "float", "date", "datetime", "bool", "json", "other"]
RiskLevel = Literal["low", "medium", "high"]


@dataclass
class FieldInfo:
    name: str
    physical_type: PhysicalType
    semantic_type: Optional[SemanticType] = None
    is_personal_data: bool = False
    is_sensitive: bool = False
    risk_level: RiskLevel = "low"


@dataclass
class DatasetSchema:
    fields: List[FieldInfo] = field(default_factory=list)
    source: Optional[str] = None
    owner: Optional[str] = None
    purpose: Optional[str] = None

    def get_field(self, name: str) -> Optional[FieldInfo]:
        return next((f for f in self.fields if f.name == name), None)
