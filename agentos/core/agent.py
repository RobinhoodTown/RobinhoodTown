from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any
from agentos.core.config import Config
from agentos.core.memory import Memory
from agentos.core.planner import Planner, Plan
from agentos.core.executor import Executor

logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    session_id: str
    goal: str
    status: str = "idle"
    current_task: str | None = None
    tokens_used: int = 0
    cost_usd: float = 0.0

class Agent:
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config.from_env()
        self.memory = Memory(self.config)
        self.planner = Planner(self.config)
        self.executor = Executor(self.config)
        self._heartbeat_task: asyncio.Task | None = None
        self._state: AgentState | None = None

    async def run(self, goal: str, session_id: str | None = None) -> dict[str, Any]:
        import uuid
        sid = session_id or str(uuid.uuid4())
        self._state = AgentState(session_id=sid, goal=goal, status="planning")
        logger.info("Agent session %s starting: %s", sid, goal[:80])

        self._heartbeat_task = asyncio.create_task(self._heartbeat(sid))
        try:
            plan: Plan = await self.planner.decompose(goal, self.memory)
            self._state.status = "executing"
            result = await self.executor.run(plan, self.memory, self._on_task)
            self._state.status = "done"
            return result
        except Exception as exc:
            self._state.status = "failed"
            logger.error("Agent session %s failed: %s", sid, exc)
            raise
        finally:
            if self._heartbeat_task:
                self._heartbeat_task.cancel()

    def _on_task(self, task_name: str) -> None:
        if self._state:
            self._state.current_task = task_name

    async def _heartbeat(self, session_id: str) -> None:
        while True:
            await asyncio.sleep(30)
            logger.debug("Heartbeat: session=%s status=%s", session_id,
                         self._state.status if self._state else "unknown")

    @property
    def state(self) -> AgentState | None:
        return self._state









