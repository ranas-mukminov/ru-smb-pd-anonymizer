from __future__ import annotations

from typing import List

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_csv_samples(path: str, n: int = 20) -> List[dict]:
    return pd.read_csv(path, nrows=n).to_dict(orient="records")
