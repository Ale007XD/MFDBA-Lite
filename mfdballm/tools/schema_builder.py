def build_tool_schema(registry):

    tools = []

    for tool in registry.tools.values():

        tools.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        })

    return tools
