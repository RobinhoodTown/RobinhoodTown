from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Any
from agentos.core.config import Config


@dataclass
class Task:
    id: str
    name: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    status: str = "pending"
    result: Any = None


@dataclass
class Plan:
    goal: str
    tasks: list[Task]
    session_id: str

    def ready_tasks(self) -> list[Task]:
        done = {t.id for t in self.tasks if t.status == "done"}
        return [
            t for t in self.tasks
            if t.status == "pending" and set(t.dependencies).issubset(done)
        ]

    def is_complete(self) -> bool:
        return all(t.status in ("done", "skipped") for t in self.tasks)


class Planner:
    def __init__(self, config: Config) -> None:
        self.config = config

    async def decompose(self, goal: str, memory: Any) -> "Plan":
        import uuid
        sid = str(uuid.uuid4())
        tasks = [
            Task(id="t0", name="gather_context", description="Gather context"),
            Task(id="t1", name="execute_main", description=goal, dependencies=["t0"]),
            Task(id="t2", name="verify_result", description="Verify", dependencies=["t1"]),
        ]
        return Plan(goal=goal, tasks=tasks, session_id=sid)

    async def replan(self, plan: Plan, failed_task: Task, error: str) -> Plan:
        failed_task.status = "failed"
        recovery = Task(
            id=f"recover-{failed_task.id}",
            name=f"recover_{failed_task.name}",
            description=f"Recover from: {error[:100]}",
            dependencies=[d for d in failed_task.dependencies],
        )
        plan.tasks.append(recovery)
        return plan






