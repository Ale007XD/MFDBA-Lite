from mfdballm.runtime.events import ModelResponseEvent


class ModelHandler:

    def __init__(self, router):
        self.router = router

    async def __call__(self, event, state):
        response = await self.router.chat(state.messages)

        return ModelResponseEvent(response=response)
