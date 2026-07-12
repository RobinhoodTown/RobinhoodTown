from __future__ import annotations
import re
from typing import Any
from agentos.tools.base import BaseTool, ToolResult

class BrowserTool(BaseTool):
    name = "browser"
    description = "Fetch and render web pages, extract structured content"

    async def execute(self, url: str = "", extract: str = "text") -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                r = await client.get(url, headers={"User-Agent": "AgentOS/0.9"})
                r.raise_for_status()
                content = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text)).strip()
                return ToolResult(success=True, output=content[:50000],
                                  metadata={"url": url, "status": r.status_code})
        except Exception as exc:
            return ToolResult(success=False, output=None, error=str(exc))

