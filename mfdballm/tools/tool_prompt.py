import json


def build_tools_prompt(tools):

    schemas = []

    for tool in tools:
        schemas.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.schema
        })

    schema_json = json.dumps(schemas, indent=2)

    return f"""
You are an AI agent.

You can call tools.

TOOLS:

{schema_json}

When calling a tool respond ONLY in JSON:

{{
 "tool": "<tool_name>",
 "args": {{...}}
}}
"""
