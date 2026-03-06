class RuntimeState:

    def __init__(self, messages=None):

        self.messages = list(messages or [])

        # runtime metrics
        self.runtime_steps = 0
        self.llm_calls = 0
        self.tool_calls = 0
