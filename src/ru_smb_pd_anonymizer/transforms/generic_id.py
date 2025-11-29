from __future__ import annotations

import pandas as pd

from .strategies.hashing import HashingStrategy
from .strategies.masking import mask_tail
from .strategies.tokenization import InMemoryTokenizer


class GenericIdHashingTransformer:
    def __init__(self, salt: str | None = None):
        self.strategy = HashingStrategy(salt=salt)

    def fit(self, series: pd.Series) -> "GenericIdHashingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return series.astype(str).apply(self.strategy.hash_value)


class GenericIdTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="id")

    def fit(self, series: pd.Series) -> "GenericIdTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)


class GenericIdMaskingTransformer:
    def __init__(self, keep: int = 3):
        self.keep = keep

    def fit(self, series: pd.Series) -> "GenericIdMaskingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return mask_tail(series.astype(str), keep=self.keep)

