from mfdballm.tools.base import Tool


class EchoTool(Tool):

    name = "echo"
    description = "Echo input text"

    schema = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string"
            }
        },
        "required": ["text"]
    }

    def run(self, text):
        return text
