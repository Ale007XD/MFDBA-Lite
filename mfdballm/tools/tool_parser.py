import json
import re


class ToolCall:
    def __init__(self, name: str, arguments: dict):
        self.name = name
        self.arguments = arguments


def parse_tool_call(text: str):
    """
    Detect tool call JSON in model output.

    Expected format:

    {
      "tool": "tool_name",
      "arguments": { ... }
    }
    """

    try:
        data = json.loads(text)

        if "tool" in data:
            return ToolCall(
                name=data["tool"],
                arguments=data.get("arguments", {})
            )

    except Exception:
        pass

    # try extracting JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group())

        if "tool" in data:
            return ToolCall(
                name=data["tool"],
                arguments=data.get("arguments", {})
            )
    except Exception:
        return None

    return None
