from dataclasses import dataclass


@dataclass
class ProviderResponse:

    text: str | None = None

    tool_calls: list | None = None
