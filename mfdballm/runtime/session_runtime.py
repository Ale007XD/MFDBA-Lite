from typing import List

from mfdballm.config import load_config
from mfdballm.provider_registry import build_providers
from mfdballm.router import Router

from mfdballm.execution.tool_executor import ToolExecutor
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

    def __init__(self):

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

        # step history (Canonical Runtime API)
        self.steps: List[StepResult] = []

    def add_step(self, step: StepResult) -> None:
        """
        Store a StepResult in runtime history.
        """
        self.steps.append(step)

    def get_steps(self) -> List[StepResult]:
        """
        Return all recorded steps.
        """
        return self.steps
