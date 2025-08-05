import asyncio
import logging
import aiohttp

from utils import async_timed, fetch_status, delay


@async_timed()
async def main():
    # as_completed - принимает список допускающих ожидание объектов и возвращает
    # итератор по будущим объектам. Эти объекты можно перебирать, применяя к
    # каждому await. Когда выражение await вернет управление, мы получим
    # результат первой завершившейся сопрограммы.

    # as_completed - простой пример
    print('.as_completed() - простой пример (время выполнения - сумма времени всех задач)')
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 5),
            fetch_status(session, 'https://www.example.com', 2)
        ]
        for finish_task in asyncio.as_completed(fetchers):
            print(await finish_task)

    print('\r\n.as_completed() - пример с таймаутом')
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 5),
            fetch_status(session, 'https://www.example.com', 2)
        ]
        for finish_task in asyncio.as_completed(fetchers, timeout=4):
            try:
                result = await finish_task
                print(result)
            except asyncio.exceptions.TimeoutError:
                logging.error('Произошел таймаут!')

        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())
