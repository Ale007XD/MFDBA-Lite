from mfdballm.parsers.action_parser import parse_provider_response
from mfdballm.types import ProviderResponse

r = ProviderResponse(text="hello")

a = parse_provider_response(r)

assert a.type.name == "FINISH"

print("ACTION PARSER TEST PASSED")
