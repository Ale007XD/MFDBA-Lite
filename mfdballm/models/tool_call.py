class ToolCall:
    """
    Represents a tool call requested by the LLM.
    """

    def __init__(self, name: str, arguments: dict):
        self.name = name
        self.arguments = arguments or {}
