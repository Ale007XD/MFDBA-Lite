import asyncio
import pytest

from mfdballm.router import Router


class SlowProvider:

    async def chat(self, messages):
        await asyncio.sleep(1)
        return {"text": "slow"}


class FastProvider:

    async def chat(self, messages):
        return {"text": "fast"}


@pytest.mark.asyncio
async def test_timeout_does_not_trip_circuit():

    router = Router([SlowProvider(), FastProvider()])

    messages = [{"role": "user", "content": "hi"}]

    result = await router.achat(messages, timeout=0.1)

    assert result == "fast"

    snapshot = router.get_health_snapshot()

    # slow provider must not be marked as failure
    assert snapshot[0]["failures"] == 0
