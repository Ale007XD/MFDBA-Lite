from mfdballm.runtime.events import (
    UserMessageEvent,
    ModelResponseEvent,
    ToolCallEvent,
    ToolResultEvent
)

from mfdballm.runtime.handlers.user_message_handler import UserMessageHandler
from mfdballm.runtime.handlers.model_response_handler import ModelResponseHandler
from mfdballm.runtime.handlers.tool_call_handler import ToolCallHandler
from mfdballm.runtime.handlers.tool_result_handler import ToolResultHandler


class EventDispatcher:

    def __init__(self):
        self.handlers = {}

    def register(self, event_type, handler):
        self.handlers[event_type] = handler

    async def dispatch(self, event, state):

        handler = self.handlers.get(type(event))

        if not handler:
            raise RuntimeError(f"No handler for {type(event)}")

        return await handler.handle(event, state)

    def register_default_handlers(self, router, tool_executor):

        self.register(
            UserMessageEvent,
            UserMessageHandler(router)
        )

        self.register(
            ModelResponseEvent,
            ModelResponseHandler()
        )

        self.register(
            ToolCallEvent,
            ToolCallHandler(tool_executor)
        )

        self.register(
            ToolResultEvent,
            ToolResultHandler(router)
        )
