from __future__ import annotations

import pandas as pd

from .strategies.generalization import keep_region_only, truncate_house
from .strategies.tokenization import InMemoryTokenizer


class AddressGeneralizationTransformer:
    def __init__(self, mode: str = "region"):
        self.mode = mode

    def fit(self, series: pd.Series) -> "AddressGeneralizationTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        if self.mode == "region":
            return keep_region_only(series)
        if self.mode == "city_street":
            return truncate_house(series)
        return series


class AddressTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="addr")

    def fit(self, series: pd.Series) -> "AddressTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)
