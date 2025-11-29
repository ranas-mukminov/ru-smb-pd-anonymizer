from __future__ import annotations

import importlib
from pathlib import Path
from typing import Annotated

import typer

from ...policies.model import Policy


def validate_policy_cmd(
    policy: Annotated[Path, typer.Option(..., "--policy", help="Policy YAML")],
) -> None:
    pol = Policy.from_yaml(str(policy))

    errors = []
    for fp in pol.fields:
        if not fp.transformer:
            continue
        if "." not in fp.transformer:
            errors.append(f"Transformer not namespaced: {fp.transformer}")
            continue
        module_name, class_name = fp.transformer.rsplit(".", 1)
        module_path = f"ru_smb_pd_anonymizer.transforms.{module_name}"
        try:
            module = importlib.import_module(module_path)
            getattr(module, class_name)
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"Cannot import {fp.transformer}: {exc}")

    if errors:
        for err in errors:
            typer.echo(err, err=True)
        raise typer.Exit(code=1)

    typer.echo("Policy is valid")
