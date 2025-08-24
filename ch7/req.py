import asyncio
import functools
import time
import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


async def main():
    loop = asyncio.get_running_loop()
    start = time.time()
    # with ThreadPoolExecutor() as pool:
    urls = ['https://www.example.com' for _ in range(1000)]
    # tasks = [loop.run_in_executor(None, functools.partial(get_status_code, url)) for url in urls]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

    print(f'Выполнение запросов завершено за {time.time() - start:.4f} с')


asyncio.run(main())
