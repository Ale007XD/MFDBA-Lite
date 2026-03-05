from mfdballm.config import load_config
from mfdballm.provider_registry import build_providers
from mfdballm.router import Router

from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.execution.tool_agent import ToolAgent

from mfdballm.tools.registry import ToolRegistry


class SessionRuntime:

    def __init__(self):

        # загрузка конфигурации
        config = load_config()

        # провайдеры
        providers = build_providers(config)

        # router
        self.router = Router(providers)

        # registry инструментов
        self.registry = ToolRegistry()

        # executor инструментов
        self.tool_executor = ToolExecutor(self.registry)

        # agent (LLM reasoning + tool loop)
        self.agent = ToolAgent(
            router=self.router,
            tool_executor=self.tool_executor,
            registry=self.registry
        )

    async def run(self, messages):

        return await self.agent.run(messages)
