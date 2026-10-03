from __future__ import annotations

import pytest

from ru_smb_pd_anonymizer.transforms.strategies.hashing import HashingStrategy


def test_explicit_salt_is_used(monkeypatch):
    monkeypatch.delenv("RU_PD_ANON_HASH_SALT", raising=False)
    strategy = HashingStrategy(salt="explicit-salt")
    assert strategy.hash_value("7701234567") == HashingStrategy(salt="explicit-salt").hash_value(
        "7701234567"
    )


def test_env_salt_used_when_constructor_omits_salt(monkeypatch):
    monkeypatch.setenv("RU_PD_ANON_HASH_SALT", "env-salt-value")
    strategy = HashingStrategy()
    assert strategy.salt == "env-salt-value"
    a = strategy.hash_value("abc")
    b = HashingStrategy(salt="env-salt-value").hash_value("abc")
    assert a == b


def test_explicit_salt_overrides_env(monkeypatch):
    monkeypatch.setenv("RU_PD_ANON_HASH_SALT", "env-salt-value")
    strategy = HashingStrategy(salt="constructor-wins")
    assert strategy.salt == "constructor-wins"


def test_missing_salt_fails_closed(monkeypatch):
    monkeypatch.delenv("RU_PD_ANON_HASH_SALT", raising=False)
    with pytest.raises(ValueError, match="RU_PD_ANON_HASH_SALT"):
        HashingStrategy()


def test_blank_env_salt_fails_closed(monkeypatch):
    monkeypatch.setenv("RU_PD_ANON_HASH_SALT", "   ")
    with pytest.raises(ValueError, match="RU_PD_ANON_HASH_SALT"):
        HashingStrategy()
