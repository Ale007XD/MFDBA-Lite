from mfdballm.runtime.events import UserMessageEvent, StopEvent
from mfdballm.runtime.event_dispatcher import EventDispatcher
from mfdballm.runtime.runtime_state import RuntimeState
from mfdballm.runtime.router_adapter import RouterAdapter


class ExecutionEngine:

    def __init__(self, router, tool_executor, max_steps=10):

        router_adapter = RouterAdapter(router)

        self.dispatcher = EventDispatcher()
        self.dispatcher.register_default_handlers(
            router_adapter,
            tool_executor
        )

        self.max_steps = max_steps

    async def run(self, messages):

        state = RuntimeState(messages=list(messages))

        event = UserMessageEvent(messages[-1])

        step = 0

        while True:

            if step > self.max_steps:
                raise RuntimeError("Runtime loop exceeded max steps")

            step += 1

            event = await self.dispatcher.dispatch(event, state)

            if isinstance(event, StopEvent):
                return event.result
