from typing import Any, Dict, Optional, List
from pydantic import BaseModel


class ProviderResponse(BaseModel):
    """
    Canonical provider response used by ExecutionEngine.

    All provider outputs must be normalized to this format.
    """

    text: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def normalize(cls, raw: Any) -> "ProviderResponse":
        """
        Normalize arbitrary provider output to ProviderResponse.

        Supported inputs:
        - ProviderResponse
        - provider-like objects (with .text / .tool_calls)
        - str
        - dict
        - OpenAI-style responses
        """

        # ---------------------------------------------------------
        # Case 1: already ProviderResponse
        # ---------------------------------------------------------
        if isinstance(raw, cls):
            return raw

        # ---------------------------------------------------------
        # Case 2: provider-like object (duck typing)
        # ---------------------------------------------------------
        if hasattr(raw, "text") or hasattr(raw, "tool_calls"):
            return cls(
                text=getattr(raw, "text", None),
                tool_calls=getattr(raw, "tool_calls", None),
            )

        # ---------------------------------------------------------
        # Case 3: None → empty response
        # ---------------------------------------------------------
        if raw is None:
            return cls(text="")

        # ---------------------------------------------------------
        # Case 4: plain string
        # ---------------------------------------------------------
        if isinstance(raw, str):
            return cls(text=raw)

        # ---------------------------------------------------------
        # Case 5: dictionary response
        # ---------------------------------------------------------
        if isinstance(raw, dict):

            text = raw.get("text")
            tool_calls = raw.get("tool_calls")

            # OpenAI-style response
            if "choices" in raw:
                choices = raw.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    text = message.get("content")
                    tool_calls = message.get("tool_calls")

            # simple format: {"content": "..."}
            if text is None and "content" in raw:
                text = raw["content"]

            # nested message: {"message": {"content": "..."}}
            if text is None and "message" in raw:
                msg = raw["message"]
                if isinstance(msg, dict):
                    text = msg.get("content")

            if text is not None or tool_calls is not None:
                return cls(text=text, tool_calls=tool_calls)

            # fallback: stringify unknown dict
            return cls(text=str(raw))

        # ---------------------------------------------------------
        # Unsupported format
        # ---------------------------------------------------------
        raise RuntimeError("ProviderResponse could not be normalized")
