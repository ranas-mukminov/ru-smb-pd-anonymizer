from __future__ import annotations

import pandas as pd


class FormatPreservingEncryptor:
    """Interface placeholder for FPE backends.

    Real cryptography is intentionally out of scope; integrate with an approved
    crypto service and supply encrypt/decrypt callables.
    """

    def __init__(self, encrypt_callable=None, decrypt_callable=None):
        self.encrypt_callable = encrypt_callable
        self.decrypt_callable = decrypt_callable

    def fit(self, series: pd.Series) -> "FormatPreservingEncryptor":
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        if not self.encrypt_callable:
            raise NotImplementedError("FPE encrypt callable is not configured")
        return series.astype(str).apply(self.encrypt_callable)

    def inverse(self, series: pd.Series) -> pd.Series:
        if not self.decrypt_callable:
            raise NotImplementedError("FPE decrypt callable is not configured")
        return series.astype(str).apply(self.decrypt_callable)
