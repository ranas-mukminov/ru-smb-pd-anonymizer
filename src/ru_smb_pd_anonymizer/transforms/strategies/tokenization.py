from __future__ import annotations

from typing import Dict, Optional

import pandas as pd


class InMemoryTokenizer:
    """Simple reversible tokenizer with in-memory mapping. Not production-grade storage."""

    def __init__(self, prefix: str = "tok", start: int = 1):
        self.prefix = prefix
        self.counter = start
        self.forward: Dict[str, str] = {}
        self.reverse: Dict[str, str] = {}

    def fit(self, series: pd.Series) -> "InMemoryTokenizer":
        for value in series.dropna().astype(str).unique():
            self._get_token(value)
        return self

    def _get_token(self, value: str) -> str:
        if value not in self.forward:
            token = f"{self.prefix}_{self.counter}"
            self.forward[value] = token
            self.reverse[token] = value
            self.counter += 1
        return self.forward[value]

    def transform(self, series: pd.Series) -> pd.Series:
        return series.astype(str).apply(lambda v: self._get_token(v) if v else v)

    def inverse(self, series: pd.Series) -> pd.Series:
        return series.apply(lambda v: self.reverse.get(v, v))
