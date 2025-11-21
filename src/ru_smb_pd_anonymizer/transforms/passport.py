from __future__ import annotations

import pandas as pd

from .base import Transformer
from .strategies.masking import mask_tail
from .strategies.tokenization import InMemoryTokenizer
from .strategies.suppression import suppress


class PassportMaskingTransformer:
    def __init__(self, keep: int = 4):
        self.keep = keep

    def fit(self, series: pd.Series) -> "PassportMaskingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return mask_tail(series.astype(str), keep=self.keep)


class PassportTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="passport")

    def fit(self, series: pd.Series) -> "PassportTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)


class PassportSuppressionTransformer:
    def fit(self, series: pd.Series) -> "PassportSuppressionTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return suppress(series)
