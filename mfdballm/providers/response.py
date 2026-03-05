from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ProviderResponse:
    """
    Unified response returned by all providers.
    """

    content: Optional[str]
    model: str
    tool_call: Optional[Dict[str, Any]] = None
