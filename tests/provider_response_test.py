import asyncio
from mfdballm.types import ProviderResponse
from mfdballm.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    async def chat(self, messages, tools=None):
        return ProviderResponse(text='hello')


async def main():

    p = DummyProvider('dummy','key','model')

    r = await p.chat([{'role':'user','content':'hi'}])

    assert isinstance(r, ProviderResponse)

    print('PROVIDER RESPONSE TEST PASSED')


asyncio.run(main())
