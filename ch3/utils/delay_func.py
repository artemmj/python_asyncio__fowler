import asyncio

from .async_timer import async_timed


@async_timed()
async def delay(delay_secs: int) -> int:
    print(f'Засыпаю на {delay_secs} с.')
    await asyncio.sleep(delay_secs)
    print(f'Сон в течение {delay_secs} с. закончился')
    return delay_secs
