import asyncio

from utils import delay


async def main():
    long_task = asyncio.create_task(delay(10))

    secs_elapsed = 0

    while not long_task.done():
        print(f'({secs_elapsed}) Задача не закончилась, следующая проверка через секунду.')
        await asyncio.sleep(1)
        secs_elapsed += 1
        if secs_elapsed == 5:
            long_task.cancel()
    
    try:
        await long_task
    except asyncio.CancelledError:
        print('Задача была снята.')

asyncio.run(main())
