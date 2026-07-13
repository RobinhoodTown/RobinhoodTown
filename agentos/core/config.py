from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import os

@dataclass
class Config:
    model: str = "claude-sonnet-5"
    max_tokens: int = 8192
    temperature: float = 0.0
    task_timeout: int = 300
    max_agents: int = 10
    memory_max_tokens: int = 8000
    tool_retry_max: int = 3
    tool_retry_base_delay: float = 1.0
    db_url: str = "sqlite:///data/agentos.db"
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "info"
    api_key: str = field(default_factory=lambda: os.environ.get("AGENTOS_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            model=os.environ.get("AGENTOS_MODEL", "claude-sonnet-5"),
            max_agents=int(os.environ.get("AGENTOS_MAX_AGENTS", "10")),
            task_timeout=int(os.environ.get("AGENTOS_TASK_TIMEOUT", "300")),
            memory_max_tokens=int(os.environ.get("AGENTOS_MEMORY_MAX_TOKENS", "8000")),
            db_url=os.environ.get("AGENTOS_DB_URL", "sqlite:///data/agentos.db"),
            log_level=os.environ.get("AGENTOS_LOG_LEVEL", "info"),
        )

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        import json
        data = json.loads(path.read_text())
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})



