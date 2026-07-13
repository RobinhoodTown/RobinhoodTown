from __future__ import annotations
import asyncio, logging, uuid
from typing import Any
from agentos.core.config import Config
from agentos.multi.message_bus import MessageBus

logger = logging.getLogger(__name__)

class Coordinator:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.bus = MessageBus()
        self._pool: list[Any] = []
        self._semaphore = asyncio.Semaphore(config.max_agents)
        self._running = False

    async def start(self) -> None:
        self._running = True
        logger.info("Coordinator started (max_agents=%d)", self.config.max_agents)

    async def stop(self) -> None:
        self._running = False
        logger.info("Coordinator stopped")

    async def submit(self, agent: Any, goal: str, **kwargs: Any) -> dict[str, Any]:
        async with self._semaphore:
            session_id = str(uuid.uuid4())
            logger.info("Submitting goal to agent session=%s", session_id)
            return await agent.run(goal, session_id=session_id, **kwargs)

    @property
    def active_count(self) -> int:
        return self.config.max_agents - self._semaphore._value


