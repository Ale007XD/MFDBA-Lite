import json
import re

TOOL_PATTERN = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)


def parse_tool_call(text: str):

    match = TOOL_PATTERN.search(text)

    if not match:
        return None

    payload = match.group(1).strip()

    try:
        return json.loads(payload)
    except Exception:
        return None
