import pytest, asyncio
from agentos.core.config import Config
from agentos.core.planner import Planner
from agentos.core.memory import Memory

@pytest.fixture
def planner(): return Planner(Config())
@pytest.fixture
def memory(): return Memory(Config())

@pytest.mark.asyncio
async def test_decompose_returns_plan(planner, memory):
    plan = await planner.decompose("write a blog post about AI agents", memory)
    assert plan.goal == "write a blog post about AI agents"
    assert len(plan.tasks) > 0

@pytest.mark.asyncio
async def test_ready_tasks_respects_dependencies(planner, memory):
    plan = await planner.decompose("test goal", memory)
    ready = plan.ready_tasks()
    for t in ready:
        assert t.dependencies == []





