from __future__ import annotations

from typing import List

import pandas as pd


def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_parquet_samples(path: str, n: int = 20) -> List[dict]:
    return pd.read_parquet(path).head(n).to_dict(orient="records")
