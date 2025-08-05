import asyncio
import aiohttp
from aiohttp import ClientSession

from utils import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str, timeout: int = 1) -> int:
    t_out = aiohttp.ClientTimeout(total=timeout)
    async with session.get(url, timeout=t_out) as result:
        return result.status


# @async_timed()
async def main():
    # Обычный асинхронный запрос
    print('Обычный асинхронный запрос')
    async with ClientSession() as session:
        url = 'https://example.com'
        status = await fetch_status(session, url)
        print(f'Состояние для {url} было равно {status}')

    # Асинхронный запрос с таймаутом
    print('\r\nАсинхронный запрос с таймаутом')
    session_timeout = aiohttp.ClientTimeout(total=2, connect=1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        result = await fetch_status(session, 'https://example.com', timeout=5)
        print(result)

asyncio.run(main())
