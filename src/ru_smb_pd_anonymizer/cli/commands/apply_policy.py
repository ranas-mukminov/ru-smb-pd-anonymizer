from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import typer

from ...dtypes.detectors import detect_fields
from ...policies.model import Policy
from ...pipeline.core import apply_policy_to_dataframe


def apply_policy_cmd(
    input: Path = typer.Option(..., "--input", help="Input dataset"),
    format: str = typer.Option("csv", "--format", help="csv|parquet"),
    schema: Optional[Path] = typer.Option(None, "--schema", help="Schema JSON"),
    policy: Path = typer.Option(..., "--policy", help="Policy YAML"),
    output: Path = typer.Option(..., "--output", help="Output dataset"),
) -> None:
    fmt = format.lower()
    if fmt == "csv":
        df = pd.read_csv(input)
    elif fmt in {"parquet", "pq"}:
        df = pd.read_parquet(input)
    else:
        typer.echo("Unsupported format", err=True)
        raise typer.Exit(code=1)

    if schema:
        import json

        schema_data = json.loads(schema.read_text(encoding="utf-8"))
        from ...dtypes.models import DatasetSchema, FieldInfo, SemanticType

        fields = [
            FieldInfo(
                name=f["name"],
                physical_type=f.get("physical_type", "string"),
                semantic_type=SemanticType(f.get("semantic_type")) if f.get("semantic_type") else None,
                is_personal_data=f.get("is_personal_data", False),
                is_sensitive=f.get("is_sensitive", False),
                risk_level=f.get("risk_level", "low"),
            )
            for f in schema_data.get("fields", [])
        ]
        ds_schema = DatasetSchema(fields=fields)
    else:
        ds_schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))

    pol = Policy.from_yaml(str(policy))
    anonymized = apply_policy_to_dataframe(df, ds_schema, pol)

    if fmt == "csv":
        anonymized.to_csv(output, index=False)
    else:
        anonymized.to_parquet(output, index=False)
