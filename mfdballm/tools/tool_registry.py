class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, name, tool):
        self._tools[name] = tool

    def get(self, name):
        if name not in self._tools:
            raise Exception(f"Tool '{name}' not registered")
        return self._tools[name]

    def list(self):
        return list(self._tools.keys())
