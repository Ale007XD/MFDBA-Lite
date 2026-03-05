from typing import Any, Dict


class Tool:
    name: str = "tool"
    description: str = ""

    async def run(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()
