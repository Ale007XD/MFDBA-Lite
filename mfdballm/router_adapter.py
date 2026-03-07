class RouterAdapter:

    def __init__(self, router):
        self.router = router

    async def call(self, messages):

        router = self.router

        if hasattr(router, "chat"):
            return await router.chat(messages)

        if hasattr(router, "route"):
            return await router.route(messages)

        if hasattr(router, "complete"):
            return await router.complete(messages)

        if hasattr(router, "generate"):
            return await router.generate(messages)

        raise RuntimeError("Router has no supported inference method")
