from __future__ import annotations
import asyncio
import logging
import signal
from typing import Any
from agentos.core.config import Config
from agentos.core.agent import Agent

logger = logging.getLogger(__name__)


class Runtime:
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config.from_env()
        self._running = False

    async def start(self) -> None:
        self._running = True
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        logger.info("AgentOS runtime started (max_agents=%d)", self.config.max_agents)

    async def stop(self) -> None:
        logger.info("Shutting down runtime...")
        self._running = False
        logger.info("Runtime stopped cleanly")

    async def run(self, goal: str, **kwargs: Any) -> dict[str, Any]:
        agent = Agent(self.config)
        return await agent.run(goal, **kwargs)

    async def __aenter__(self) -> "Runtime":
        await self.start()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()










