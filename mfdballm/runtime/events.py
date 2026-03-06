class Event:
    pass


class UserMessageEvent(Event):

    def __init__(self, message):
        self.message = message


class ModelResponseEvent(Event):

    def __init__(self, response):
        self.response = response


class ToolCallEvent(Event):

    def __init__(self, tool_calls):
        self.tool_calls = tool_calls


class ToolResultEvent(Event):

    def __init__(self, result):
        self.result = result


class StopEvent(Event):

    def __init__(self, result):
        self.result = result
