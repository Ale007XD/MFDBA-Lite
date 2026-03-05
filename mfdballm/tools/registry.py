from typing import Callable, Dict


class ToolRegistry:
    """
    Registry of available tools.
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        """
        Register a tool function.
        """

        self.tools[name] = func

    def get_tools(self) -> Dict[str, Callable]:
        """
        Return all registered tools.
        """

        return self.tools
