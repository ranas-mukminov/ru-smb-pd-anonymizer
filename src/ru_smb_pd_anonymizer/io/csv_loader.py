from __future__ import annotations

from typing import Any, List, cast

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_csv_samples(path: str, n: int = 20) -> List[dict[str, Any]]:
    records = pd.read_csv(path, nrows=n).to_dict(orient="records")
    return cast(List[dict[str, Any]], records)
