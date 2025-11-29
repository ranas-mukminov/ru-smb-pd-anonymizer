from __future__ import annotations

import random
from typing import Optional

import pandas as pd


def add_numeric_noise(
    series: pd.Series, scale: float = 1.0, seed: Optional[int] = None
) -> pd.Series:
    rng = random.Random(seed)
    return series.apply(
        lambda v: v + rng.uniform(-scale, scale) if isinstance(v, (int, float)) else v
    )
