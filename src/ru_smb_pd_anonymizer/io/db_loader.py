from __future__ import annotations

from typing import List

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


def load_query(engine: Engine, query: str, limit: int | None = None) -> pd.DataFrame:
    sql = query if limit is None else f"{query} LIMIT {int(limit)}"
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def load_query_samples(engine: Engine, query: str, n: int = 20) -> List[dict]:
    df = load_query(engine, query, limit=n)
    return df.to_dict(orient="records")
