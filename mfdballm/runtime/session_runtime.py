from typing import List, Dict, Any

from mfdballm.config import load_config
from mfdballm.provider_registry import build_providers
from mfdballm.router import Router

from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.tools.registry import ToolRegistry

from mfdballm.models.step_result import StepResult


class SessionRuntime:
    """
    Runtime container for a single session execution.

    Responsibilities:
    - hold router
    - hold tool executor
    - hold tool registry
    - store StepResult history

    Does NOT implement agent loop or orchestration.
    ExecutionEngine controls the execution flow.
    """

    def __init__(self) -> None:

        # configuration
        config = load_config()

        # providers
        providers = build_providers(config)

        # router
        self.router = Router(providers)

        # tool registry
        self.registry = ToolRegistry()

        # tool executor
        self.tool_executor = ToolExecutor(self.registry)

        # execution engine
        self.engine = ExecutionEngine(
            self.router,
            self.tool_executor,
        )

        # step history
        self.steps: List[StepResult] = []

    async def run(self, messages: List[Dict[str, Any]]) -> Any:
        """
        Runtime entrypoint used by tests and CLI.
        Delegates execution to the ExecutionEngine.
        """
        return await self.engine.run(messages)

    def add_step(self, step: StepResult) -> None:
        """
        Store a StepResult in runtime history.
        """
        self.steps.append(step)

    def get_steps(self) -> List[StepResult]:
        """
        Return all recorded steps.
        """
        return list(self.steps)
