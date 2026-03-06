from mfdballm.runtime.events import ModelResponseEvent


class UserMessageHandler:

    def __init__(self, router):
        self.router = router

    async def handle(self, event, state):

        # сообщение уже находится в state.messages
        response = await self.router.complete(state.messages)

        return ModelResponseEvent(response)
