from __future__ import annotations

from typing import Protocol

import pandas as pd


class Transformer(Protocol):
    def fit(self, series: pd.Series) -> "Transformer":
        ...

    def transform(self, series: pd.Series) -> pd.Series:
        ...

    def inverse(self, series: pd.Series) -> pd.Series:
        """Optional inverse for reversible transforms."""
        raise NotImplementedError
