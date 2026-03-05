import json


def execute_tool(name, args, tools):

    """
    Executes tool by name.
    """

    for tool in tools:

        if tool.name == name:
            return tool.run(**args)

    raise Exception(f"Tool '{name}' not found")
