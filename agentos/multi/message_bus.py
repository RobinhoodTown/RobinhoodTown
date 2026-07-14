from __future__ import annotations
import asyncio, logging
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)

@dataclass
class Message:
    id: str
    sender: str
    recipient: str
    payload: Any
    reply_to: str | None = None

class MessageBus:
    def __init__(self) -> None:
        self._queues: dict[str, asyncio.Queue] = {}
        self._subscribers: dict[str, list[Callable]] = {}

    def register(self, agent_id: str) -> None:
        if agent_id not in self._queues:
            self._queues[agent_id] = asyncio.Queue()

    async def send(self, message: Message) -> None:
        if message.recipient not in self._queues:
            raise KeyError(f"Agent not registered: {message.recipient}")
        await self._queues[message.recipient].put(message)
        logger.debug("Bus: %s -> %s", message.sender, message.recipient)

    async def receive(self, agent_id: str, timeout: float = 30.0) -> Message:
        q = self._queues.get(agent_id)
        if not q:
            raise KeyError(f"Agent not registered: {agent_id}")
        return await asyncio.wait_for(q.get(), timeout=timeout)



