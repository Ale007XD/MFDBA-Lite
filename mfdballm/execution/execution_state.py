class ExecutionState:

    def __init__(self, messages):

        self.messages = list(messages)

        self.tool_results = []

        self.iteration = 0

    def add_tool_result(self, result):

        self.tool_results.append(result)

    def increment(self):

        self.iteration += 1
