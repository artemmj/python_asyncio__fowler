import asyncio
import os
import sys
import tty
from asyncio import StreamReader
from collections import deque

from read_line import read_line
from cursor_helpers import (
    delete_line,
    move_to_bottom_of_screen,
    move_to_top_of_screen,
    restore_cursor_position,
    save_cursor_position,
)
from message_store import MessageStore


async def create_stdin_reader() -> StreamReader:
    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader


async def sleep(delay: int, message_store: MessageStore):
    """Добавить выходное сообщение в хранилище."""
    await message_store.append(f'Начало задержки {delay}')
    await asyncio.sleep(delay)
    await message_store.append(f'Конец задержки {delay}')


async def main():
    tty.setcbreak(sys.stdin)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    async def redraw_output(items: deque):
        """
        Обратный вызов, который перемещает курсор в начало экрана,
        перерисовывает экран и возвращает курсор обратно.
        """
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_position()

    messages = MessageStore(redraw_output, rows - 1)
    stdin_reader = await create_stdin_reader()

    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, messages))


if __name__ == '__main__':
    asyncio.run(main())
