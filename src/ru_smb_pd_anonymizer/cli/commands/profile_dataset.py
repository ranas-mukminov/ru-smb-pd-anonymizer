from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import pandas as pd
import typer

from ...classification.risk_model import score_dataset
from ...classification.sample_profiler import profile_dataframe
from ...dtypes.detectors import detect_fields


def profile_dataset_cmd(
    input_path: Annotated[Path, typer.Option(..., "--input", help="Input dataset")],
    format: Annotated[str, typer.Option("csv", "--format", help="csv|parquet")],
    out: Annotated[Optional[Path], typer.Option(None, "--out", help="Output JSON")],
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
    profile = profile_dataframe(df)
    risk = score_dataset(df, schema)
    output = {
        "profile": {k: vars(v) for k, v in profile.fields.items()},
        "risk": risk,
    }
    content = json.dumps(output, ensure_ascii=False, indent=2)
    if out:
        out.write_text(content, encoding="utf-8")
    else:
        typer.echo(content)
