from __future__ import annotations
import asyncio
import pytest
from agentos.core.config import Config
from agentos.core.runtime import Runtime

@pytest.fixture
def config():
    return Config(max_agents=2, task_timeout=10, memory_max_tokens=1000)

@pytest.mark.asyncio
async def test_runtime_start_stop(config):
    async with Runtime(config) as rt:
        assert rt._running

@pytest.mark.asyncio
async def test_runtime_run_goal(config):
    rt = Runtime(config)
    await rt.start()
    result = await rt.run("summarise the README")
    await rt.stop()
    assert isinstance(result, dict)





