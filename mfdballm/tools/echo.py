from .base import Tool


class EchoTool(Tool):

    name = "echo"
    description = "Echo input text"

    async def run(self, text: str):
        return {"echo": text}
