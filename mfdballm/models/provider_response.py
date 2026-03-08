from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    Canonical tool call representation used by ExecutionEngine.
    """

    id: Optional[str] = None
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ProviderResponse(BaseModel):
    """
    Canonical LLM response used by Router and ExecutionEngine.

    Providers SHOULD return this model directly.
    Router will normalize compatible outputs automatically.

    Supported provider return types:
        - ProviderResponse
        - str
        - dict
    """

    text: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)

    model_config = {
        "extra": "ignore"
    }

    # ---------------------------------------------------------
    # Normalization layer (Router contract)
    # ---------------------------------------------------------

    @staticmethod
    def normalize(value: Any) -> "ProviderResponse":
        """
        Convert provider outputs into canonical ProviderResponse.

        Accepted inputs:
            ProviderResponse
            str
            dict
        """

        # Already normalized
        if isinstance(value, ProviderResponse):
            return value

        # Simple string response
        if isinstance(value, str):
            return ProviderResponse(text=value)

        # Dict-based response
        if isinstance(value, dict):

            text = value.get("text")

            tool_calls_raw = value.get("tool_calls", [])

            tool_calls = []

            for call in tool_calls_raw:

                if isinstance(call, ToolCall):
                    tool_calls.append(call)

                elif isinstance(call, dict):

                    tool_calls.append(
                        ToolCall(
                            id=call.get("id"),
                            name=call.get("name"),
                            arguments=call.get("arguments", {})
                        )
                    )

            return ProviderResponse(
                text=text,
                tool_calls=tool_calls
            )

        raise TypeError(
            f"Unsupported provider response type: {type(value)}"
        )
