from mfdballm.types_tool_call import ToolCall


def main():

    c = ToolCall(
        name="echo",
        arguments={"text": "hello"}
    )

    assert c.name == "echo"

    assert c.arguments["text"] == "hello"

    print("TOOL CALL TEST PASSED")


if __name__ == "__main__":
    main()
