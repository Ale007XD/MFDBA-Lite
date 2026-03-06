import asyncio

from mfdballm.types import ProviderResponse
from mfdballm.types_tool_call import ToolCall
from mfdballm.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    async def generate(self, prompt):
        return ProviderResponse(
            text="hello",
            tool_calls=[
                ToolCall(
                    name="echo",
                    arguments={"text": "hi"}
                )
            ]
        )

    @property
    def metadata(self):
        return None


async def main():

    p = DummyProvider()

    r = await p.generate("hi")

    assert isinstance(r, ProviderResponse)

    assert r.tool_calls[0].name == "echo"

    print("PROVIDER RESPONSE TEST PASSED")


asyncio.run(main())
