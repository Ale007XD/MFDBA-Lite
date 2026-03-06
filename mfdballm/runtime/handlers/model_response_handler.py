from mfdballm.runtime.events import ToolCallEvent, StopEvent


class ModelResponseHandler:

    async def handle(self, event, state):

        response = event.response

        # добавляем ответ модели в историю
        if getattr(response, "text", None):
            state.messages.append({
                "role": "assistant",
                "content": response.text
            })

        # если модель вызвала инструменты
        if getattr(response, "tool_calls", None):
            return ToolCallEvent(response.tool_calls)

        # финальный ответ
        return StopEvent(response.text)
