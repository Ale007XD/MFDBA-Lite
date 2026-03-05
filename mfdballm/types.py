from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ProviderResponse:
    text: str
    raw: Optional[Dict[str, Any]] = None
