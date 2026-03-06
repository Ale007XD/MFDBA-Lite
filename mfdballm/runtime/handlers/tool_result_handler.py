from mfdballm.runtime.events import ModelResponseEvent


class ToolResultHandler:

    def __init__(self, router):
        self.router = router

    async def handle(self, event, state):

        results = event.result

        if not isinstance(results, list):
            results = [results]

        for r in results:
            state.messages.append({
                "role": "tool",
                "content": str(r)
            })

        response = await self.router.complete(state.messages)

        return ModelResponseEvent(response)
