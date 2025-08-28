import asyncio
import asyncpg
import os
import tty
from collections import deque
from asyncpg.pool import Pool

from message_store import MessageStore
from read_line import read_line
from cursor_helpers import (
    delete_line,
    move_to_bottom_of_screen,
    move_to_top_of_screen,
    restore_cursor_position,
    save_cursor_position,
)
from stdin_reader import create_stdin_reader


async def run_query(query: str, pool: Pool, message_store: MessageStore):
    print(f'in run_query(): {query}')
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchrow(query)
            await message_store.append(f'Выбрано {len(result)} строк по запросу: {query} ({result})')
        except Exception as exc:
            await message_store.append(f'Получено исключение {exc} от: {query}')


async def main():
    tty.setcbreak(0)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    async def redraw_output(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_position()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()

    async with asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password1',
        database='products',
        min_size=6,
        max_size=6,
    ) as pool:
        while True:
            print('in cycle')
            query = await read_line(stdin_reader)
            asyncio.create_task(run_query(query, pool, messages))


if __name__ == '__main__':
    asyncio.run(main())
