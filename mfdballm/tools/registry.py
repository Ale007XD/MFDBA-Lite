class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, name, tool=None):

        # register(tool)
        if tool is None:

            tool = name
            name = getattr(tool, "name", tool.__class__.__name__)

        name = name.lower()

        if name in self.tools:
            raise ValueError(f"Tool already registered: {name}")

        self.tools[name] = tool

    def get(self, name):

        if name is None:
            return None

        return self.tools.get(name.lower())

    def list_tools(self):

        return sorted(self.tools.keys())
