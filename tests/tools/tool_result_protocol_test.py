from mfdballm.types_tool_result import ToolResult


def main():

    r = ToolResult(
        tool_name="echo",
        output="hello",
        success=True
    )

    assert r.tool_name == "echo"

    assert r.success is True

    print("TOOL RESULT PROTOCOL TEST PASSED")


if __name__ == "__main__":
    main()
