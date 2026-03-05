from mfdballm.tools.schema_builder import build_tool_schema
from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.base import BaseTool


class EchoTool(BaseTool):

    name = "echo"
    description = "echo text"

    async def run(self, args):
        return args["text"]


registry = ToolRegistry()
registry.register(EchoTool())

schema = build_tool_schema(registry)

assert schema[0]["name"] == "echo"

print("TOOL SCHEMA TEST PASSED")
