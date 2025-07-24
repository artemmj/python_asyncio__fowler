import asyncio

from utils import delay


async def main():
    task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Таймаут!')
        print(f'Задача была снята? {task.cancelled()}')

asyncio.run(main())
