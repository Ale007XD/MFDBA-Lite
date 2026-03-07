from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ProviderResponse:

    text: str

    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, response):

        text = None
        tool_calls = []
        metadata = {}

        # --- dict responses (common in tests / simple routers)
        if isinstance(response, dict):

            for field_name in ("text", "content", "message", "output"):
                if field_name in response:
                    text = response[field_name]
                    break

            tool_calls = response.get("tool_calls", [])
            metadata = response.get("metadata", {})

        # --- object responses (OpenAI-style / provider SDKs)
        else:

            for field_name in ("text", "content", "message", "output"):
                if hasattr(response, field_name):
                    text = getattr(response, field_name)
                    break

            tool_calls = getattr(response, "tool_calls", [])
            metadata = getattr(response, "metadata", {})

        if text is None and not tool_calls:
            raise RuntimeError("ProviderResponse has neither text nor tool_calls")

        return cls(
            text=text,
            tool_calls=tool_calls,
            metadata=metadata
        )
