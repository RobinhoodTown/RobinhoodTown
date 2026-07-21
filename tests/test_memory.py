from __future__ import annotations
import asyncio
import pytest
from agentos.core.config import Config
from agentos.core.memory import Memory, MemoryEntry

@pytest.fixture
def memory():
    config = Config(memory_max_tokens=100)
    return Memory(config)

@pytest.mark.asyncio
async def test_add_and_search(memory):
    await memory.add("the quick brown fox jumps over the lazy dog", importance=1.0)
    results = await memory.search("fox jumps")
    assert len(results) >= 1
    assert "fox" in results[0].content

@pytest.mark.asyncio
async def test_compression_fires(memory):
    for i in range(50):
        await memory.add(f"entry {i} " + "word " * 10)
    assert memory._token_count <= memory.config.memory_max_tokens * 1.1

@pytest.mark.asyncio
async def test_context_window_respects_limit(memory):
    for i in range(10):
        await memory.add(f"context chunk {i} " + "word " * 20)
    ctx = memory.context_window(max_tokens=50)
    assert len(ctx.split()) <= 60











