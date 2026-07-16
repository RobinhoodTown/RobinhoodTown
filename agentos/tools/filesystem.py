from __future__ import annotations
from pathlib import Path
from typing import Any
from agentos.tools.base import BaseTool, ToolResult

class FilesystemTool(BaseTool):
    name = "filesystem"
    description = "Read, write, list files within the workspace"

    def __init__(self, *args: Any, workspace: Path | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.workspace = workspace or Path.cwd()

    def _safe(self, path: str) -> Path:
        target = (self.workspace / path).resolve()
        if not str(target).startswith(str(self.workspace)):
            raise ValueError("Path traversal denied")
        return target

    async def execute(self, action: str = "read", path: str = "", content: str = "") -> ToolResult:
        try:
            if action == "read":
                return ToolResult(success=True, output=self._safe(path).read_text(errors="replace"))
            if action == "write":
                p = self._safe(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)
                return ToolResult(success=True, output=f"Written {len(content)} bytes")
            if action == "list":
                entries = [str(f.relative_to(self.workspace)) for f in self._safe(path).iterdir()]
                return ToolResult(success=True, output=entries)
            return ToolResult(success=False, output=None, error=f"Unknown action: {action}")
        except Exception as exc:
            return ToolResult(success=False, output=None, error=str(exc))





