import asyncio
from agentos import Runtime, Agent, Config
from agentos.multi.coordinator import Coordinator

async def main():
    config = Config(max_agents=4)
    coordinator = Coordinator(config)
    await coordinator.start()

    tasks = [
        "fetch and summarise the HN front page",
        "search for recent papers on multi-agent systems",
        "check the status of our GitHub Actions workflows",
    ]
    results = await asyncio.gather(*[
        coordinator.submit(Agent(config), goal)
        for goal in tasks
    ])
    for goal, result in zip(tasks, results):
        print(f"\n--- {goal} ---")
        print(result)

    await coordinator.stop()

if __name__ == "__main__":
    asyncio.run(main())





