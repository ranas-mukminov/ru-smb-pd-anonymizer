from __future__ import annotations

import pandas as pd
from typing import Protocol


class Transformer(Protocol):
    def fit(self, series: pd.Series) -> "Transformer":
        ...

    def transform(self, series: pd.Series) -> pd.Series:
        ...

    def inverse(self, series: pd.Series) -> pd.Series:
        """Optional inverse for reversible transforms."""
        raise NotImplementedError
