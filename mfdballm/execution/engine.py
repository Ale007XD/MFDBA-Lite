from typing import Optional, Dict, Any
from mfdballm.execution.agent import BaseAgent


class ExecutionResult:

    def __init__(self, output: str, metadata: Optional[Dict[str, Any]] = None):
        self.output = output
        self.metadata = metadata or {}


class ExecutionEngine:

    def __init__(self, agent: BaseAgent):
        self.agent = agent

    async def run(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:

        context = context or {}

        result = await self.agent.run(message)

        return ExecutionResult(
            output=result,
            metadata=context
        )
