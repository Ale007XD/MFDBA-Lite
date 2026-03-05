from mfdballm.models.tool_call import ToolCall


def parse_tool_calls(provider_response):
    """
    Convert provider response tool calls into normalized ToolCall objects.
    """

    tool_calls = provider_response.tool_calls

    if not tool_calls:
        return []

    parsed = []

    for call in tool_calls:
        name = call.get("name")
        arguments = call.get("arguments", {})

        parsed.append(ToolCall(name=name, arguments=arguments))

    return parsed
