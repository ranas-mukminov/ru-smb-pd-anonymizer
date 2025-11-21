from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import yaml


class AnonymizationLevel(str, Enum):
    NONE = "NONE"
    PSEUDONYMIZED_REVERSIBLE = "PSEUDONYMIZED_REVERSIBLE"
    PSEUDONYMIZED_ONE_WAY = "PSEUDONYMIZED_ONE_WAY"
    ANONYMIZED_IRREVERSIBLE = "ANONYMIZED_IRREVERSIBLE"


@dataclass
class FieldPolicy:
    field_pattern: str
    level: AnonymizationLevel
    transformer: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    name: str
    description: str
    use_case: str
    fields: List[FieldPolicy] = field(default_factory=list)
    global_rules: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Policy":
        fields = [
            FieldPolicy(
                field_pattern=f.get("field_pattern", ""),
                level=AnonymizationLevel(f.get("level", "NONE")),
                transformer=f.get("transformer"),
                params=f.get("params", {}),
            )
            for f in data.get("fields", [])
        ]
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            use_case=data.get("use_case", ""),
            fields=fields,
            global_rules=data.get("global_rules", {}),
        )

    @classmethod
    def from_yaml(cls, path: str) -> "Policy":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "use_case": self.use_case,
            "fields": [
                {
                    "field_pattern": f.field_pattern,
                    "level": f.level.value,
                    "transformer": f.transformer,
                    "params": f.params,
                }
                for f in self.fields
            ],
            "global_rules": self.global_rules,
        }

    def to_yaml(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, allow_unicode=True, sort_keys=False)
