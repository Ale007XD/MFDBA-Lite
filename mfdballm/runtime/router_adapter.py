class RouterAdapter:

    def __init__(self, router):
        self.router = router

    async def complete(self, messages):
        """
        Unified router interface.

        Supported router APIs:
        - router.complete(messages)
        - router.chat(messages)
        - router.run(messages)
        - router.generate(messages)
        - router(messages)
        """

        if hasattr(self.router, "complete"):
            return await self.router.complete(messages)

        if hasattr(self.router, "chat"):
            return await self.router.chat(messages)

        if hasattr(self.router, "run"):
            return await self.router.run(messages)

        if hasattr(self.router, "generate"):
            return await self.router.generate(messages)

        if callable(self.router):
            result = self.router(messages)

            if hasattr(result, "__await__"):
                return await result

            return result

        raise RuntimeError(
            "Router has no compatible interface (complete/chat/run/generate/callable)"
        )
