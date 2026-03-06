from dataclasses import dataclass


@dataclass
class ProviderMetadata:

    name: str

    models: list

    supports_tools: bool = True

    supports_stream: bool = False

    max_context_tokens: int = 4096
