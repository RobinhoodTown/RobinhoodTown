# API Reference

## Runtime

```python
class Runtime:
    async def start(self) -> None
    async def stop(self) -> None
    async def run(self, goal: str, **kwargs) -> dict[str, Any]
```

## Agent

```python
class Agent:
    async def run(self, goal: str, session_id: str | None = None) -> dict[str, Any]
    state: AgentState | None
```

## Memory

```python
class Memory:
    async def add(self, content: str, importance: float = 1.0) -> str
    async def search(self, query: str, top_k: int = 5) -> list[MemoryEntry]
    def context_window(self, max_tokens: int = 4000) -> str
```

## Tools

All tools share the same interface:

```python
class BaseTool:
    async def run(self, **kwargs) -> ToolResult
```

`ToolResult`:
- `success: bool`
- `output: Any`
- `error: str | None`
- `metadata: dict`
