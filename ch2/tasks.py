import asyncio

from utils import delay, async_timed


async def hello_every_second():
    for _ in range(4):
        await asyncio.sleep(1)
        print("hello_every_second(): исполнятется, другой код ожидает долгую операцию")


@async_timed()
async def main():
    # Выполнение кода, пока другие операции работают
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay
    print()

    # Снятие долгой задачи (не самый лучший, но возможный способ)
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
        print('Выброшено исключение CancelledError, задача была снята.')
    print()

    # Задание таймаута с помощью wait_for
    task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Таймаут!')
        print(f'Задача была снята? {task.cancelled()}')
    print()

    # Защита задачи от снятия
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Задача заняла более 5 с, скоро она закончится!")
        result = await task
        print(result)


asyncio.run(main())
