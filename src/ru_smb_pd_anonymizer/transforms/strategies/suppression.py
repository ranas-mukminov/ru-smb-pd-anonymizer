from __future__ import annotations

import pandas as pd


def suppress(series: pd.Series) -> pd.Series:
    return series.apply(lambda _: None)
