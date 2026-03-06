from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ProviderResponse:

    text: str

    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, response):

        # deterministic text extraction
        for field_name in ("text", "content", "message", "output"):

            if hasattr(response, field_name):

                text = getattr(response, field_name)

                break
        else:

            raise RuntimeError("ProviderResponse has no text field")

        tool_calls = getattr(response, "tool_calls", [])

        metadata = getattr(response, "metadata", {})

        return cls(
            text=text,
            tool_calls=tool_calls,
            metadata=metadata
        )
