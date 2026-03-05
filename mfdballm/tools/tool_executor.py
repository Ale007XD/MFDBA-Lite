def execute_tool(call):

    tool = TOOL_REGISTRY[call.name]

    return tool.run(**call.args)
