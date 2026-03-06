class RuntimeStateMachine:

    IDLE = "IDLE"
    LLM_CALL = "LLM_CALL"
    TOOL_EXEC = "TOOL_EXEC"
    FINISHED = "FINISHED"

    def __init__(self):
        self.state = self.IDLE
        self.trace = [self.state]

    def transition_to_llm(self):
        self.state = self.LLM_CALL
        self.trace.append(self.state)

    def transition_to_tool(self):
        self.state = self.TOOL_EXEC
        self.trace.append(self.state)

    def finish(self):
        self.state = self.FINISHED
        self.trace.append(self.state)

    def is_finished(self):
        return self.state == self.FINISHED

    def get_trace(self):
        return list(self.trace)
