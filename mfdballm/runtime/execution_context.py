from typing import Any, Dict, List, Optional


class ExecutionContext:
    """
    Runtime execution context passed through the pipeline.

    Stores:
    - conversation messages
    - available tools
    - execution metadata
    """

    def __init__(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.messages: List[Dict[str, Any]] = messages or []
        self.tools: Dict[str, Any] = tools or {}
        self.metadata: Dict[str, Any] = metadata or {}

    def add_message(self, message: Dict[str, Any]) -> None:
        """
        Append message to conversation history.
        """
        self.messages.append(message)

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Return conversation messages.
        """
        return self.messages

    def get_tool(self, name: str):
        """
        Retrieve tool by name.
        """
        return self.tools.get(name)

    def register_tool(self, name: str, tool: Any) -> None:
        """
        Register tool inside context.
        """
        self.tools[name] = tool
