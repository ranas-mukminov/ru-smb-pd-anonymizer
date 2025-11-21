from ru_smb_pd_anonymizer.ai.base import NoopAIProvider
from ru_smb_pd_anonymizer.ai.field_classifier import suggest_semantics
from ru_smb_pd_anonymizer.ai.policy_suggester import suggest_policy


def test_noop_provider_returns_stub():
    provider = NoopAIProvider()
    assert "noop" in provider.complete("test")
    assert "noop" in provider.chat([])


def test_suggest_semantics_returns_schema():
    schema = suggest_semantics(["fio", "email"], samples=[])
    names = [f.name for f in schema.fields]
    assert "fio" in names


def test_policy_suggester_stub():
    policy = suggest_policy("analytics", {"fio": "FIO"})
    assert policy.name.startswith("suggested")
