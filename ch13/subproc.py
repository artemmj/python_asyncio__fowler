import asyncio
from asyncio.subprocess import Process


async def main():
    process1: Process = await asyncio.create_subprocess_exec('ls', '-l')
    print(f'pid process1: {process1.pid}')
    try:
        status_code1 = await process1.wait()
        # status_code2 = await asyncio.wait_for(process2.wait(), timeout=3.0)
        print(f'Код состояния 1: {status_code1}')
    except asyncio.TimeoutError:
        print('Тайм-аут, завершаю принудительно...')
        process1.terminate()
        status_code1 = await process1.wait()
        print(status_code1)


if __name__ == '__main__':
    asyncio.run(main())
