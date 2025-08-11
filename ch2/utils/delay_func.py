import asyncio

from .async_timer import async_timed


# @async_timed()
async def delay(delay_secs: int):
    print(f'delay(): засыпаю=работаю на {delay_secs} с.')
    await asyncio.sleep(delay_secs)
    print(f'delay(): сон=работа в течение {delay_secs} с. закончился')
