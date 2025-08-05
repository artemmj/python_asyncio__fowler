import asyncio
import aiohttp

from utils import async_timed, fetch_status, delay


@async_timed()
async def main():
    # gather - для конкурентного выполнения допускающих ожидание объектов
    # Основная проблема: необходимость дождаться завершения всех допускающих ожидания,
    # объектов, прежде чем станет возможен доступ к результатам. Это проблема,
    # если требуется обрабатывать результаты в темпе их получения. А также
    # в случае, когда одни объекты завершаются быстро, а другие медленно,
    # потому что gather будет ждать завершения всех.

    print('\r\nВыполняется обычный .gather(delay(3), delay(1))')
    results = await asyncio.gather(delay(3), delay(1))
    print(results)

    # gather -  с передачей списка сопрограмм
    print('\r\nВыполняется .gather() с передачей списка сопрограмм')
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(10)]
        # status_codes = [await fetch_status(session, url) for url in urls]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

    urls = [
        'https://example.com',
        'https://ya.ru',
        'python://example.com',
        'https://microsoft.com',
        'https://vk.ru',
    ]

    # gather - обработка исключений
    print('\r\nРабота с обработкой исключений - .gather(return_exceptions=False)')
    print('... возбудится исключение ...')
    # async with aiohttp.ClientSession() as session:
    #     tasks = [fetch_status(session, url) for url in urls]
    #     results = await asyncio.gather(*tasks, return_exceptions=False)

    print('\r\nабота с обработкой исключений - .gather(return_exceptions=True)')
    print('... исключение будет в results, можно отфильтровать ...')
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'Все результаты: {len(results)}: {results}')
        print(f'Завершились успешно: {len(successful_results)}: {successful_results}')
        print(f'Завершились с исключением: {len(exceptions)}: {exceptions}')

asyncio.run(main())
