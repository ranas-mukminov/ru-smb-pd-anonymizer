from __future__ import annotations

import pandas as pd

from .strategies.masking import mask_email
from .strategies.tokenization import InMemoryTokenizer


class EmailMaskingTransformer:
    def fit(self, series: pd.Series) -> "EmailMaskingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return mask_email(series.astype(str))


class EmailTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="email")

    def fit(self, series: pd.Series) -> "EmailTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)
