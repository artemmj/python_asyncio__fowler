import asyncio
from asyncio.subprocess import Process


async def main():
    program = ['python3', 'big_data.py']
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        stdout=asyncio.subprocess.PIPE,
    )
    print(f'pid процесса: {process.pid}')
    # return_code = await process.wait()
    # print(f'Процесс вернул: {return_code}')
    stdout, stderr = await process.communicate()
    print(stdout)
    print(stderr)
    print(f'Процесс вернул: {process.returncode}')


if __name__ == '__main__':
    asyncio.run(main())
