#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if command -v pip-audit >/dev/null 2>&1; then
  pip-audit || true
fi
if command -v safety >/dev/null 2>&1; then
  safety check || true
fi
if command -v bandit >/dev/null 2>&1; then
  bandit -r src || true
fi
