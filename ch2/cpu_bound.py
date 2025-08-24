import asyncio

from utils import delay, async_timed


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for _ in range(100_000_000):
        counter += 1
    return counter

# Конкурентное выполнение нескольких задач

@async_timed()
async def main():
    task_1 = asyncio.create_task(cpu_bound_work())
    task_2 = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))

    await task_1
    await task_2
    await delay_task


asyncio.run(main())  # debug=True
