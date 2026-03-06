from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ProviderMetadata:
    """
    Static provider capability description.

    This data is used by routing and health monitoring layers.
    """

    name: str
    models: List[str]
    supports_tools: bool
    supports_stream: bool
    max_context_tokens: int
