from __future__ import annotations
import asyncio, os, tempfile
from agentos.tools.base import BaseTool, ToolResult

class CodeTool(BaseTool):
    name = "code"
    description = "Execute Python code in a sandboxed subprocess"

    async def execute(self, code: str = "", timeout: int = 30) -> ToolResult:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code); path = f.name
        try:
            proc = await asyncio.create_subprocess_exec(
                "python3", path,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                return ToolResult(success=False, output=None, error=f"Timed out after {timeout}s")
            if proc.returncode == 0:
                return ToolResult(success=True, output=stdout.decode()[:10000])
            return ToolResult(success=False, output=stdout.decode(), error=stderr.decode())
        finally:
            os.unlink(path)





