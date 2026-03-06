from mfdballm.types_tool_result import ToolResult


r = ToolResult(
    tool_name='echo',
    output='hello',
    success=True
)

assert r.tool_name == 'echo'
assert r.output == 'hello'
assert r.success is True

print('TOOL RESULT TEST PASSED')
