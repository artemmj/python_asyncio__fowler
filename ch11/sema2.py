import asyncio
from asyncio import Semaphore, BoundedSemaphore


async def acquire(semaphore: Semaphore):  # BoundedSemaphore
    print('Ожидание возможности захвата...')
    async with semaphore:
        print('... захвачен')
        await asyncio.sleep(5)
    print('Освобождается...')


async def release(semaphore: Semaphore):  # BoundedSemaphore
    print('Одиночное освобождение...')
    semaphore.release()
    print('Одиночное освобождение - готово...')


async def main():
    semaphore = Semaphore(2)  # BoundedSemaphore

    print(">> Два захвата, три освобождения...")
    await asyncio.gather(
        acquire(semaphore),
        acquire(semaphore),
        release(semaphore),
    )

    print(">> Три захвата...")
    await asyncio.gather(
        acquire(semaphore),
        acquire(semaphore),
        acquire(semaphore),
    )


if __name__ == '__main__':
    asyncio.run(main())
