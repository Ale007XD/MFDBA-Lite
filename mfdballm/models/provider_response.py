from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ProviderResponse:
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
