from mfdballm.provider_registry import ProviderRegistry
from mfdballm.router import Router

from mfdballm.execution.engine import ExecutionEngine
from mfdballm.execution.agent import BaseAgent

from mfdballm.tools.registry import ToolRegistry


class DefaultAgent(BaseAgent):
    """
    Minimal runtime agent.

    Delegates generation to router.
    """

    def __init__(self, router: Router):
        self.router = router

    async def run(self, messages):

        response = await self.router.chat(messages)

        # Providers may return either str or object with .text
        if isinstance(response, str):
            return response

        if hasattr(response, "text"):
            return response.text

        return str(response)


class SessionRuntime:
    """
    Production runtime container.
    Builds the full runtime environment.
    """

    def __init__(self):

        # Providers
        self.provider_registry = ProviderRegistry()
        self.provider_registry.load_from_env()

        providers = self.provider_registry.get_providers()

        # Router
        self.router = Router(providers)

        # Tools
        self.tool_registry = ToolRegistry()

        # Agent
        self.agent = DefaultAgent(self.router)

        # Execution engine
        self.engine = ExecutionEngine(self.agent)

    async def run(self, messages):

        result = await self.engine.run(messages)

        return result
