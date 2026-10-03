from __future__ import annotations

import hashlib
import os
from typing import Optional

# Documented in README troubleshooting / security guidance.
_HASH_SALT_ENV = "RU_PD_ANON_HASH_SALT"


class HashingStrategy:
    """Deterministic hashing with salt for pseudonymization.

    Salt resolution order:
    1. Explicit ``salt=`` constructor argument
    2. ``RU_PD_ANON_HASH_SALT`` environment variable

    A random default is intentionally refused: silent random salts made
    hashes non-reproducible across runs while README documented
    ``RU_PD_ANON_HASH_SALT`` that was never read.
    """

    def __init__(self, salt: Optional[str] = None, algorithm: str = "sha256"):
        resolved = (salt if salt is not None else None) or os.environ.get(_HASH_SALT_ENV)
        if isinstance(resolved, str):
            resolved = resolved.strip()
        if not resolved:
            raise ValueError(
                "HashingStrategy requires an explicit salt for deterministic "
                "pseudonymization. Pass salt=... to the transformer, set "
                f"params.salt in the policy YAML, or export {_HASH_SALT_ENV}. "
                "Refusing a random default so hashes stay reproducible across runs."
            )
        self.salt = resolved
        self.algorithm = algorithm

    def hash_value(self, value: str) -> str:
        digest = hashlib.new(self.algorithm)
        digest.update(f"{self.salt}:{value}".encode("utf-8"))
        return digest.hexdigest()
