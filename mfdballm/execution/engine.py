from mfdballm.execution.agent import BaseAgent


class ExecutionEngine:
    """
    Core execution orchestrator.

    The engine is intentionally simple and only delegates
    execution to the provided agent.

    Architecture principle:
        Engine orchestrates
        Agent contains reasoning
    """

    def __init__(self, agent: BaseAgent):
        self.agent = agent

    async def run(self, message: str):
        """
        Execute a message through the agent.
        """
        result = await self.agent.run(message)

        return result
