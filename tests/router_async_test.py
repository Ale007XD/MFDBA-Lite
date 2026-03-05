import asyncio

from mfdballm.router import Router


class FakeProvider:

    name = "fake"

    async def chat(self, messages):

        return "ok"


async def run_test():

    router = Router([FakeProvider()])

    result = await router.chat([
        {"role": "user", "content": "hello"}
    ])

    assert result == "ok"

    print("Router async test OK")


if __name__ == "__main__":

    asyncio.run(run_test())
