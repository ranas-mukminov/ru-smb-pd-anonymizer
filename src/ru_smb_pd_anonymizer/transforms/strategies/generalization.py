from __future__ import annotations

import pandas as pd


def keep_region_only(series: pd.Series) -> pd.Series:
    """Heuristic: keep first token (region/city) and drop granular parts."""
    return series.astype(str).apply(lambda v: v.split(",")[0].strip() if v else v)


def truncate_house(series: pd.Series) -> pd.Series:
    def _truncate(address: str) -> str:
        parts = address.split(",")
        return ",".join(parts[:2]).strip()

    return series.astype(str).apply(lambda v: _truncate(v) if v else v)
