from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import pandas as pd
import typer

from ...dtypes.detectors import detect_fields


def inspect_schema_cmd(
    input_path: Annotated[Path, typer.Option(..., "--input", help="Input file")],
    format: Annotated[str, typer.Option("csv", "--format", help="Input format: csv|parquet")],
    out: Annotated[Optional[Path], typer.Option(None, "--out", help="Output schema JSON")],
) -> None:
    fmt = format.lower()
    if fmt == "csv":
        df = pd.read_csv(input_path)
    elif fmt in {"parquet", "pq"}:
        df = pd.read_parquet(input_path)
    else:
        typer.echo("Unsupported format", err=True)
        raise typer.Exit(code=1)

    schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
    data = {
        "fields": [
            {
                "name": f.name,
                "physical_type": f.physical_type,
                "semantic_type": f.semantic_type.value if f.semantic_type else None,
                "is_personal_data": f.is_personal_data,
                "is_sensitive": f.is_sensitive,
                "risk_level": f.risk_level,
            }
            for f in schema.fields
        ]
    }
    output_text = json.dumps(data, ensure_ascii=False, indent=2)
    if out:
        out.write_text(output_text, encoding="utf-8")
    else:
        typer.echo(output_text)
