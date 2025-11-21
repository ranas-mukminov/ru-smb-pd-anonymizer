#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

python - <<'PY'
import time
import pandas as pd
from ru_smb_pd_anonymizer.dtypes.detectors import detect_fields
from ru_smb_pd_anonymizer.pipeline.core import apply_policy_to_dataframe
from ru_smb_pd_anonymizer.policies.model import Policy

rows = 100000
chunk = {
    "customer_id": range(rows),
    "fio": ["Иванов Иван Иванович"] * rows,
    "phone": ["+7 999 123-45-67"] * rows,
    "email": ["user@example.com"] * rows,
}
df = pd.DataFrame(chunk)
schema = detect_fields(df.columns, df.head(50).to_dict(orient="records"))
policy = Policy.from_yaml("src/ru_smb_pd_anonymizer/policies/builtin/analytics.yaml")
start = time.time()
_ = apply_policy_to_dataframe(df, schema, policy)
elapsed = time.time() - start
print(f"Processed {len(df)} rows in {elapsed:.2f}s")
PY
