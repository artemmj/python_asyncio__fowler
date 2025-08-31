import asyncio
from asyncio import Lock

lock = Lock()


async def a():  # async def a(lock: Lock):
    print('Сопрограмма (А) ждет возможности захватить блокировку')
    async with lock:
        print('... (А) захватила блокировку, выполняет что-то... ')
        await asyncio.sleep(3)
        print('... (А) выполнила работу... ')
    print('Сопрограмма (A) освободила блокировку')


async def b():  # async def b(lock: Lock):
    print('Сопрограмма (B) ждет возможности захватить блокировку')
    async with lock:
        print('... (B) захватила блокировку, выполняет что-то... ')
        await asyncio.sleep(2)
        print('... (B) выполнила работу... ')
    print('Сопрограмма (B) освободила блокировку')


async def main():
    # lock = Lock()
    # await asyncio.gather(b(lock), a(lock))
    await asyncio.gather(a(), b())


if __name__ == '__main__':
    asyncio.run(main())
