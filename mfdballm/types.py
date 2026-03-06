from dataclasses import dataclass
from typing import List, Optional

from mfdballm.types_tool_call import ToolCall


@dataclass
class ProviderResponse:

    text: str

    tool_calls: Optional[List[ToolCall]] = None
