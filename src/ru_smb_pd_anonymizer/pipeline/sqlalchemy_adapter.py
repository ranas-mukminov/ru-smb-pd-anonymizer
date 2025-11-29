from __future__ import annotations

from typing import Optional

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from ..dtypes.detectors import detect_fields
from ..policies.model import Policy
from .core import apply_policy_to_dataframe


def anonymize_table(
    engine: Engine,
    source_sql: str,
    destination_table: str,
    policy: Policy,
    schema_name: Optional[str] = None,
    chunksize: int = 10000,
) -> None:
    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(text(source_sql))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
        anonymized = apply_policy_to_dataframe(df, schema, policy)
        anonymized.to_sql(
            destination_table,
            conn,
            index=False,
            if_exists="replace",
            schema=schema_name,
            chunksize=chunksize,
        )
