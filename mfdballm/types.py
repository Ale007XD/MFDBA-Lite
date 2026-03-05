from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from mfdballm.types_tool import ToolCall


@dataclass
class ProviderResponse:
    """
    Universal response returned by all LLM providers
    """

    text: str | None
    tool_calls: Optional[List[ToolCall]] = None
    raw: Optional[Dict[str, Any]] = None
