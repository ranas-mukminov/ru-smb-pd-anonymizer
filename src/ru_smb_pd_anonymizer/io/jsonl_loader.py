from __future__ import annotations

import json
from typing import List

import pandas as pd


def load_jsonl(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return pd.DataFrame(rows)


def load_jsonl_samples(path: str, n: int = 20) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        rows = [json.loads(line) for idx, line in enumerate(f) if line.strip() and idx < n]
    return rows
