from __future__ import annotations

import hashlib
import secrets
from typing import Optional


class HashingStrategy:
    """Deterministic hashing with salt for pseudonymization."""

    def __init__(self, salt: Optional[str] = None, algorithm: str = "sha256"):
        self.salt = salt or secrets.token_hex(8)
        self.algorithm = algorithm

    def hash_value(self, value: str) -> str:
        digest = hashlib.new(self.algorithm)
        digest.update(f"{self.salt}:{value}".encode("utf-8"))
        return digest.hexdigest()
