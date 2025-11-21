#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if command -v ruff >/dev/null 2>&1; then
  ruff check src tests
fi
if command -v mypy >/dev/null 2>&1; then
  mypy src
fi
if command -v yamllint >/dev/null 2>&1; then
  yamllint src/ru_smb_pd_anonymizer/policies examples/configs
fi
