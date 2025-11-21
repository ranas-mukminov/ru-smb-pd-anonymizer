from __future__ import annotations

from typing import Protocol


class AIProvider(Protocol):
    def complete(self, prompt: str) -> str:
        ...

    def chat(self, messages: list[dict]) -> str:
        ...


class NoopAIProvider:
    """Offline stub that never sends data outward."""

    def complete(self, prompt: str) -> str:
        return "[noop] completion is disabled; enable external AI explicitly"

    def chat(self, messages: list[dict]) -> str:
        return "[noop] chat is disabled; enable external AI explicitly"
