import asyncio
import logging
from typing import Callable, Awaitable


class TooManyRetries(Exception):
    pass


async def retry(
    coro: Callable[[], Awaitable],
    max_retries: int,
    timeout: float,
    retry_interval: float,
):
    for retry_num in range(1, max_retries + 1):
        try:
            print(f'Пробую запрос в корутине {coro}')
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            logging.exception(
                f'Во время ожидания произошло исключение (попытка {retry_num})), пробую еще раз...',
                exc_info=e,
            )
        await asyncio.sleep(retry_interval)
    raise TooManyRetries()


async def main():

    async def always_fail():
        raise Exception('Я грохнулся!')

    async def always_timeout():
        await asyncio.sleep(1)

    try:
        await retry(always_fail, max_retries=3, timeout=5, retry_interval=.4)
    except TooManyRetries:
        print('Прошло слишком много попыток!')


if __name__ == '__main__':
    asyncio.run(main())
