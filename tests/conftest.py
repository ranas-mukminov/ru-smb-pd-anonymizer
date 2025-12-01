"""Test configuration for ensuring project imports work from source."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

# Ensure project root and ``src`` are on sys.path so tests can import code and bundled examples
# without requiring an installed package.
for path in (PROJECT_ROOT, SRC_PATH):
    str_path = str(path)
    if str_path not in sys.path:
        sys.path.insert(0, str_path)
