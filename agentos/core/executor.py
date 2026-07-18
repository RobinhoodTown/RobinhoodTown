from __future__ import annotations
import asyncio
import logging
from typing import Callable, Any
from agentos.core.config import Config
from agentos.core.planner import Plan, Task

logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, config: Config) -> None:
        self.config = config

    async def run(
        self,
        plan: Plan,
        memory: Any,
        on_task: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        results: dict[str, Any] = {}
        while not plan.is_complete():
            ready = plan.ready_tasks()
            if not ready:
                await asyncio.sleep(0.05)
                continue
            done = await asyncio.gather(
                *[self._run_task(t, memory, on_task) for t in ready],
                return_exceptions=True,
            )
            for task, result in zip(ready, done):
                if isinstance(result, Exception):
                    logger.error("Task %s failed: %s", task.name, result)
                    task.status = "failed"
                else:
                    task.status = "done"
                    task.result = result
                    results[task.name] = result
                    await memory.add(f"Completed {task.name}")
        return results

    async def _run_task(
        self,
        task: Task,
        memory: Any,
        on_task: Callable[[str], None] | None,
    ) -> Any:
        if on_task:
            on_task(task.name)
        async with asyncio.timeout(self.config.task_timeout):
            context = memory.context_window()
            await asyncio.sleep(0)
            return f"done: {task.description[:80]}"








