from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.tool_executor import ToolExecutor


def hello_tool():

    return "Hello from tool"


def main():

    registry = ToolRegistry()

    registry.register("hello_tool", hello_tool)

    tools = registry.get_tools()

    executor = ToolExecutor(tools)

    result = executor.execute("hello_tool", {})

    print("TOOL RESULT:", result)


if __name__ == "__main__":
    main()
