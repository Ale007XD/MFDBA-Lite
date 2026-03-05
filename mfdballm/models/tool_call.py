class ToolCall:
    """
    Normalized tool call representation independent from provider format.
    """

    def __init__(self, name: str, arguments: dict):
        self.name = name
        self.arguments = arguments or {}

    def __repr__(self):
        return f"ToolCall(name={self.name}, arguments={self.arguments})"
