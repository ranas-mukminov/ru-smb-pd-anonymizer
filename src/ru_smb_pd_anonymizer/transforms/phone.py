from __future__ import annotations

import pandas as pd

from .strategies.masking import mask_tail
from .strategies.tokenization import InMemoryTokenizer


class PhoneMaskingTransformer:
    def __init__(self, keep: int = 4):
        self.keep = keep

    def fit(self, series: pd.Series) -> "PhoneMaskingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return mask_tail(series.astype(str), keep=self.keep)


class PhoneTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="phone")

    def fit(self, series: pd.Series) -> "PhoneTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)
