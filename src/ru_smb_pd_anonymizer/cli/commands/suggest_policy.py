from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Optional

import typer

from ...ai.policy_suggester import suggest_policy
from ...policies.model import Policy

BUILTIN_MAP = {
    "analytics": "analytics.yaml",
    "ml_training": "ml_training.yaml",
    "tech_support": "tech_support.yaml",
    "logs": "logs_minimal.yaml",
}


def suggest_policy_cmd(
    schema: Path = typer.Option(..., "--schema", help="Path to schema JSON"),
    use_case: str = typer.Option(
        ..., "--use-case", help="analytics|ml_training|tech_support|logs"
    ),
    out: Optional[Path] = typer.Option(None, "--out", help="Where to write policy YAML"),
) -> None:
    if use_case in BUILTIN_MAP:
        path = resources.files("ru_smb_pd_anonymizer.policies.builtin").joinpath(
            BUILTIN_MAP[use_case]
        )
        policy = Policy.from_yaml(str(path))
    else:
        schema_data = json.loads(schema.read_text(encoding="utf-8"))
        overview = {f["name"]: f.get("semantic_type") for f in schema_data.get("fields", [])}
        policy = suggest_policy(use_case=use_case, schema_overview=overview)

    if out:
        policy.to_yaml(out)
    else:
        typer.echo(json.dumps(policy.to_dict(), ensure_ascii=False, indent=2))
