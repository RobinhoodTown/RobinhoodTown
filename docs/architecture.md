# Architecture

AgentOS is built on four layers: planning, execution, memory, and tools.

## Planning layer

The planner receives a natural language goal and produces a directed acyclic graph of tasks.
Each task has typed inputs, typed outputs, and a dependency list. The planner resolves
the execution order, identifies parallelisable branches, and emits a `Plan` object.

## Execution layer

The executor walks the task graph. Tasks with no pending dependencies are dispatched
concurrently via `asyncio.gather`. Each task runs inside an `asyncio.timeout` context
so long-running tasks cannot block the executor indefinitely.

## Memory layer

Three-tier memory system:

| Tier | Scope | Backend | Eviction |
|------|-------|---------|----------|
| Working | In-flight session | In-process list | Importance-based on overflow |
| Episodic | Session-scoped | SQLite | LRU after session close |
| Semantic | Cross-session | Vector index | Manual or scheduled distillation |

## Tools layer

Tools are stateless, typed, versioned, and sandboxed. Every call goes through the
`BaseTool.run()` wrapper which handles retry with exponential backoff, result caching,
and audit logging. Tool calls are non-blocking — they run inside the executor task loop.

## Multi-agent layer

The coordinator manages an agent pool bounded by `max_agents`. It exposes a typed
`MessageBus` for inter-agent communication. Agents can fan out sub-goals to the
coordinator and await results without holding their concurrency slot.







