from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import typer

from ...dtypes.detectors import detect_fields
from ...pipeline.core import apply_policy_to_dataframe
from ...policies.model import Policy


def apply_policy_cmd(
    input_path: Path = typer.Option(..., "--input", help="Input dataset"),
    policy: Path = typer.Option(..., "--policy", help="Policy YAML"),
    output: Path = typer.Option(..., "--output", help="Output dataset"),
    schema: Optional[Path] = typer.Option(None, "--schema", help="Schema JSON"),
    format: str = typer.Option("csv", "--format", help="csv|parquet"),
    report: bool = typer.Option(
        False, "--report", help="Print a short summary of anonymization for stakeholders"
    ),
) -> None:
    fmt = format.lower()
    if fmt == "csv":
        df = pd.read_csv(input_path)
    elif fmt in {"parquet", "pq"}:
        df = pd.read_parquet(input_path)
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
                semantic_type=(
                    SemanticType(f.get("semantic_type")) if f.get("semantic_type") else None
                ),
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
    if report:
        anonymized, summary = apply_policy_to_dataframe(
            df, ds_schema, pol, return_report=True
        )
    else:
        anonymized = apply_policy_to_dataframe(df, ds_schema, pol)

    if fmt == "csv":
        anonymized.to_csv(output, index=False)
    else:
        anonymized.to_parquet(output, index=False)

    if report:
        typer.echo(f"Политика: {summary.policy_name}")
        typer.echo(f"Строк обработано: {summary.rows_processed}")
        if summary.columns_anonymized:
            typer.echo("Анонимизированные поля:")
            for col, transformer in summary.columns_anonymized.items():
                typer.echo(f"  - {col}: {transformer}")
        if summary.columns_skipped:
            typer.echo("Поля без трансформации:")
            for col in summary.columns_skipped:
                typer.echo(f"  - {col}")
