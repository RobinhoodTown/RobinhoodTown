import asyncio
from agentos import Runtime

async def main():
    async with Runtime() as rt:
        result = await rt.run(
            "research the latest developments in AI agent frameworks "
            "and write a 500-word summary to report.md"
        )
        print("Done:", result)

if __name__ == "__main__":
    asyncio.run(main())





