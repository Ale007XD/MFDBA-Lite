import json
import re
from typing import Dict, Any, Optional


class ToolCallParser:
    """
    Parses tool calls from LLM responses.

    Supports:
    - structured tool calls
    - TOOLCALL> textual format
    """

    TOOL_PATTERN = r"TOOLCALL>\s*(\[[^\]]+\])"

    @staticmethod
    def parse(text: str) -> Optional[Dict[str, Any]]:

        if not text:
            return None

        match = re.search(ToolCallParser.TOOL_PATTERN, text)

        if not match:
            return None

        try:

            calls = json.loads(match.group(1))

            if not calls:
                return None

            call = calls[0]

            return {
                "name": call["name"],
                "arguments": call.get("arguments", {})
            }

        except Exception:

            return None
