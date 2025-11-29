from __future__ import annotations

import pandas as pd


def mask_tail(series: pd.Series, keep: int = 4, mask_char: str = "*") -> pd.Series:
    def _mask(value: object) -> str:
        text = "" if value is None else str(value)
        if len(text) <= keep:
            return text
        masked = mask_char * max(len(text) - keep, 0) + text[-keep:]
        return masked

    return series.apply(_mask)


def mask_email(series: pd.Series, mask_char: str = "*") -> pd.Series:
    def _mask(value: object) -> str:
        text = "" if value is None else str(value)
        if "@" not in text:
            return mask_tail(pd.Series([text]), keep=3, mask_char=mask_char).iloc[0]
        local, domain = text.split("@", 1)
        if len(local) <= 2:
            masked_local = mask_char * len(local)
        else:
            masked_local = local[0] + (mask_char * (len(local) - 2)) + local[-1]
        return f"{masked_local}@{domain}"

    return series.apply(_mask)
