from mfdballm.types import ProviderResponse
from mfdballm.types_tool import ToolCall


r = ProviderResponse(
    text=None,
    tool_calls=[
        ToolCall(
            name="echo",
            arguments={"text": "hi"}
        )
    ]
)

assert r.tool_calls[0].name == "echo"

print("PROVIDER TOOL RESPONSE TEST PASSED")
