# AgentOS

AgentOS is a production-grade runtime for autonomous AI agents. It handles the full lifecycle of agent execution — task planning, memory management, tool orchestration, multi-agent coordination, and observability — in a single coherent framework designed to run unattended at scale.

---

## What it does

AgentOS takes a goal and runs it to completion. It breaks goals into tasks, assigns tasks to the right agents, routes tool calls, manages context across long sessions, and retries intelligently when things fail. When multiple agents collaborate, AgentOS coordinates them through a typed message bus with guaranteed delivery.

The runtime targets sub-100ms task dispatch latency and has been load-tested at 100 concurrent agents on commodity hardware.

---

## Core concepts

**Agent** — an autonomous executor that takes a goal, builds a plan, and carries it out using available tools. Agents are stateless between sessions; all state lives in the memory layer.

**Planner** — decomposes a goal into a dependency graph of subtasks. Supports recursive decomposition, parallel branches, and rollback on failure.

**Memory** — three-tier: working (in-process), episodic (session-scoped SQLite), semantic (vector index with cosine similarity). Compression fires automatically on context overflow.

**Tools** — sandboxed, typed, versioned. Browser, code interpreter, file system, search, and a plugin system for custom tools. All calls are retried with exponential backoff and logged to the audit trail.

**Coordinator** — manages agent pools, distributes tasks, handles agent failure, and scales pool size based on queue depth.

---

## Performance

Load test results (100 concurrent agents, 10-tool task chain):

```
p50 task dispatch     18ms
p95 task dispatch     74ms
p99 task dispatch     98ms
memory retrieval p99   4ms  (10k entries)
tool call overhead     2ms
throughput            840 tasks/sec
```

---

## Quickstart

```bash
pip install agentos
agentos init my-agent
cd my-agent
agentos run --goal "summarise the last 7 days of HN and save to report.md"
```

---

## Architecture

```
goal
 |
 v
Planner  --[task graph]-->  Executor
                               |
                    +----------+----------+
                    |          |          |
                  Tool-1    Tool-2    Sub-agent
                    |                    |
                    +-----> Memory <------+
                               |
                          Coordinator
```

---

## Repository layout

```
agentos/
  core/        agent, runtime, planner, executor, memory, config
  tools/       browser, code, filesystem, search, base
  plugins/     loader, sandboxing, dependency resolution
  multi/       coordinator, message bus
docs/          architecture, quickstart, API reference
examples/      simple agent, multi-agent workflow
tests/         unit, integration, property-based, load
```

---

## License

MIT











