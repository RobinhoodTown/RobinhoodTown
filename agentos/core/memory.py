from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Any
from agentos.core.config import Config


@dataclass
class MemoryEntry:
    id: str
    content: str
    importance: float = 1.0
    tier: str = "working"


class Memory:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._working: list[MemoryEntry] = []
        self._episodic: list[MemoryEntry] = []
        self._lock = asyncio.Lock()
        self._token_count = 0

    async def add(self, content: str, importance: float = 1.0) -> str:
        import uuid
        entry = MemoryEntry(id=str(uuid.uuid4()), content=content, importance=importance)
        async with self._lock:
            self._working.append(entry)
            self._token_count += len(content.split())
            if self._token_count > self.config.memory_max_tokens:
                await self._compress()
        return entry.id

    async def search(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        async with self._lock:
            all_entries = self._working + self._episodic
            qw = set(query.lower().split())
            scored = sorted(
                all_entries,
                key=lambda e: len(qw & set(e.content.lower().split())) * e.importance,
                reverse=True,
            )
            return scored[:top_k]

    async def _compress(self) -> None:
        self._working.sort(key=lambda e: e.importance)
        cut = max(1, len(self._working) // 3)
        for e in self._working[:cut]:
            e.tier = "episodic"
            self._episodic.append(e)
        self._working = self._working[cut:]
        self._token_count = sum(len(e.content.split()) for e in self._working)

    def context_window(self, max_tokens: int = 4000) -> str:
        entries = sorted(self._working, key=lambda e: e.importance, reverse=True)
        result, count = [], 0
        for e in entries:
            t = len(e.content.split())
            if count + t > max_tokens:
                break
            result.append(e.content)
            count += t
        return "\n\n".join(result)







