from mfdballm.types import ProviderResponse
from mfdballm.types_tool import ToolCall

r = ProviderResponse(text='hi')

c = ToolCall(
    name='echo',
    arguments={'text':'hi'}
)

assert r.text == 'hi'
assert c.name == 'echo'

print('TYPES IMPORT TEST PASSED')
