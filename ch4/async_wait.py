import asyncio
import logging
import aiohttp

from utils import async_timed, fetch_status


@async_timed()
async def main():
    # .wait() - похожа на gather, но дает более точный контроль над ситуацией - возвращает
    # два множества: задачи, завершившиеся успешно или в результате исключения, а также
    # задачи, которые продолжают выполняться. Позволяет задать тайм-аут, который не
    # возбуждает исключений.

    print('\r\n.wait(return_when=asyncio.ALL_COMPLETED) - поведение по умолчанию')
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://www.microsoft.com', 1)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', 2)),
            asyncio.create_task(fetch_status(session, 'https://www.ya.ru', 3)),
            # asyncio.create_task(fetch_status(session, 'https://www.vk.com', 4))
        ]
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.ALL_COMPLETED)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            result = await done_task
            print(result)

    print('\r\n.wait(return_when=asyncio.FIRST_EXCEPTION)')
    print('... если возникло исключение, wait() немедленно возвращается ...')
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'h://www.microsoft.com', 1)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', 2)),
            asyncio.create_task(fetch_status(session, 'https://www.ya.ru', 3)),
        ]
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            if not done_task.exception():
                print(done_task.result())
            else:
                logging.error(f"При выполнении запроса возникло исключение: {done_task.exception()}")
        for pending_task in pending:
            pending_task.cancel()

    print('\r\n.wait(return_when=asyncio.FIRST_COMPLETED)')
    print('... wait() озвращает управление, как только получен хотя бы один результат ...')
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://www.microsoft.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
            asyncio.create_task(fetch_status(session, 'https://www.ya.ru')),
        ]
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            print(await done_task)

    print('\r\n.wait(return_when=asyncio.FIRST_COMPLETED)')
    print('... модифицированная версия, чтобы обработать остальные результаты по мере завершения/поступления ...')
    async with aiohttp.ClientSession() as session:
        pending = [
            asyncio.create_task(fetch_status(session, 'https://www.microsoft.com', delay=1)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=2)),
            asyncio.create_task(fetch_status(session, 'https://www.ya.ru', delay=3)),
        ]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            print(f'Число завершившихся задач: {len(done)}')
            print(f'Число ожидающих задач: {len(pending)}')
            for done_task in done:
                print(await done_task)

    print('\r\n.wait() - обработка таймаутов')
    async with aiohttp.ClientSession() as session:
        pending = [
            asyncio.create_task(fetch_status(session, 'https://www.microsoft.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com')),
            asyncio.create_task(fetch_status(session, 'https://www.ya.ru', delay=3)),
        ]
        done, pending = await asyncio.wait(pending, timeout=1)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            print(await done_task)

asyncio.run(main())
