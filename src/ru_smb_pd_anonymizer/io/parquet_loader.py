from __future__ import annotations

import pandas as pd
from typing import List


def load_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_parquet_samples(path: str, n: int = 20) -> List[dict]:
    return pd.read_parquet(path).head(n).to_dict(orient="records")
