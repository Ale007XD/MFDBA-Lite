class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, name, tool=None):

        # register(tool)
        if tool is None:

            tool = name
            name = getattr(tool, "name", tool.__class__.__name__.lower())

        self.tools[name] = tool

    def get(self, name):

        return self.tools.get(name)

    def list_tools(self):

        return list(self.tools.keys())
