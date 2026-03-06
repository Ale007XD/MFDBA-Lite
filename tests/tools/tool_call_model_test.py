from mfdballm.types_tool import ToolCall


c = ToolCall(
    name="echo",
    arguments={"text": "hello"}
)

assert c.name == "echo"
assert c.arguments["text"] == "hello"

print("TOOL CALL MODEL TEST PASSED")
