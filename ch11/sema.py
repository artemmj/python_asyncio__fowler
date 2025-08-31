import asyncio
from asyncio import Semaphore
from aiohttp import ClientSession


async def oper(semaphore: Semaphore):
    print('Жду возможности захватить семафор...')
    async with semaphore:
        print('... семафор захвачен')
        await asyncio.sleep(2)
    print('Семафор освобожден...')


async def get_url(url: str, session: ClientSession, semaphore: Semaphore):
    print('Жду возможности захватить семафор...')
    async with semaphore:
        print('Семафор захвачен, отправляется запрос...')
        resp = await session.get(url)
        print('Запрос завершен')
        return resp.status


async def main():
    # semaphore = Semaphore(3)
    # await asyncio.gather(*[oper(semaphore) for _ in range(4)])

    sema = Semaphore(10)
    async with ClientSession() as sess:
        tasks = [get_url('https://www.example.com', sess, sema) for _ in range(1000)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
