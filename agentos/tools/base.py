from __future__ import annotations
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from agentos.core.config import Config

logger = logging.getLogger(__name__)

@dataclass
class ToolResult:
    success: bool
    output: Any
    error: str | None = None
    metadata: dict = field(default_factory=dict)

class BaseTool(ABC):
    name: str = ""
    description: str = ""
    version: str = "1.0.0"

    def __init__(self, config: Config) -> None:
        self.config = config
        self._cache: dict[str, ToolResult] = {}

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult: ...

    async def run(self, **kwargs: Any) -> ToolResult:
        for attempt in range(self.config.tool_retry_max):
            try:
                result = await self.execute(**kwargs)
                if result.success:
                    return result
            except Exception as exc:
                if attempt == self.config.tool_retry_max - 1:
                    return ToolResult(success=False, output=None, error=str(exc))
                await asyncio.sleep(self.config.tool_retry_base_delay * (2 ** attempt))
        return ToolResult(success=False, output=None, error="max retries exceeded")








