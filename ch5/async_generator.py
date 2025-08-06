import asyncio

from utils import async_timed, delay


async def positive_ints_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer


@async_timed()
async def main():
    async_generator = positive_ints_async(5)
    print(f'type(async_generator): {type(async_generator)}')
    async for number in async_generator:
        print(f'Получено число: {number}\r\n')


asyncio.run(main())
