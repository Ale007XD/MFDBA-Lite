from typing import Dict, Any, Callable


def build_tool_schema(name: str, description: str, parameters: Dict[str, Any]):

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }


def build_schemas(tools: Dict[str, Callable]):

    schemas = []

    for name in tools.keys():

        schema = build_tool_schema(
            name=name,
            description=f"Tool: {name}",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )

        schemas.append(schema)

    return schemas
