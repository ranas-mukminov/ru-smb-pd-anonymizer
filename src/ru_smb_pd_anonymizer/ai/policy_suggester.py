from __future__ import annotations

from typing import Dict, Optional

from ..policies.model import FieldPolicy, Policy, AnonymizationLevel
from .base import AIProvider, NoopAIProvider


def suggest_policy(
    use_case: str,
    schema_overview: Dict[str, str],
    provider: Optional[AIProvider] = None,
    allow_external: bool = False,
) -> Policy:
    """Return a stub policy suggestion.

    External AI calls are disabled unless allow_external=True and a provider is passed.
    """

    fields = [
        FieldPolicy(field_pattern=f"name:{name}", level=AnonymizationLevel.PSEUDONYMIZED_ONE_WAY)
        for name in schema_overview.keys()
    ]
    policy = Policy(
        name=f"suggested_{use_case}",
        description=f"Suggested policy for {use_case}",
        use_case=use_case,
        fields=fields,
        global_rules={},
    )

    if not allow_external or provider is None or isinstance(provider, NoopAIProvider):
        return policy

    _ = provider.complete(f"Suggest anonymization levels for {use_case}")
    return policy
