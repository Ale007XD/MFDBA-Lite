class ExecutionTrace:

    def __init__(self):

        self.steps = []

    def add(self, event):

        self.steps.append(event)
