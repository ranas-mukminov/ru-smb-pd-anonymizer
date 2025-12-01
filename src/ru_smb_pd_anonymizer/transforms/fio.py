from __future__ import annotations

import pandas as pd

from .strategies.tokenization import InMemoryTokenizer


class FioMaskingTransformer:
    def __init__(self, mask_char: str = "*"):
        self.mask_char = mask_char

    def fit(self, series: pd.Series) -> "FioMaskingTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        def _mask_fio(value: object) -> str:
            text = "" if value is None else str(value)
            parts = [p for p in text.split() if p]
            if not parts:
                return text
            surname = parts[0]
            initials_list: list[str] = []
            for p in parts[1:]:
                first_char = p[0].upper()
                ascii_char = first_char.encode("ascii", "ignore").decode() or "I"
                initials_list.append(f"{ascii_char}.")
            initials = "".join(initials_list)
            return f"{surname} {initials}".strip()

        return series.apply(_mask_fio)


class FioTokenizationTransformer:
    def __init__(self, tokenizer: InMemoryTokenizer | None = None):
        self.tokenizer = tokenizer or InMemoryTokenizer(prefix="fio")

    def fit(self, series: pd.Series) -> "FioTokenizationTransformer":
        self.tokenizer.fit(series.astype(str))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.transform(series.astype(str))

    def inverse(self, series: pd.Series) -> pd.Series:
        return self.tokenizer.inverse(series)


class FioSyntheticTransformer:
    """Generate synthetic names preserving dataset size."""

    SYNTHETIC_NAMES = [
        "Иванов И.И.",
        "Петров П.П.",
        "Сидорова С.С.",
        "Кузнецов К.К.",
    ]

    def fit(self, series: pd.Series) -> "FioSyntheticTransformer":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        names = self.SYNTHETIC_NAMES
        s = series.reset_index(drop=True)
        synthetic = [names[i % len(names)] for i in range(len(s))]
        synthetic_series = pd.Series(synthetic)
        synthetic_series.index = series.index
        return synthetic_series
