import asyncio
from asyncio import Future


async def set_future_value(future: Future):
    await asyncio.sleep(1)
    # Ждать 1 с, прежде чем установить значение
    future.set_result(42)


def make_request() -> Future:
    future = Future()
    # Создать задачу, которая асинхронно установит значение future
    asyncio.create_task(set_future_value(future))
    return future


async def main():
    future = make_request()
    print(f'Будущий объект готов? {future.done()}')
    # Приостановить main, пока значение future не установлено
    value = await future
    print(f'Будущий объект готов? {future.done()}')
    print(value)


asyncio.run(main())
