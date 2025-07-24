import asyncio

from utils import delay, async_timed


async def hello_every_second():
    for _ in range(2):
        await asyncio.sleep(1)
        print("Я жду, исполняется другой код!")


@async_timed()
async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    await hello_every_second()
    await first_delay
    await second_delay

asyncio.run(main())
