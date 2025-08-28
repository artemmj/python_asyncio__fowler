import sys
from asyncio import StreamReader
from collections import deque

from cursor_helpers import move_back_one_char, clear_line


async def read_line(stdin_reader: StreamReader) -> str:
    def erase_last_char():
        """Функция для удаления предыдущего символа из стандартного вывода."""
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()

    delete_char = b'\x7f'
    input_buffer = deque()

    while (input_char := await stdin_reader.read(1)) != b'\n':
        # Если введен символ забоя, то удалить предыдущий символ
        if input_char == delete_char:
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_char()
                sys.stdout.flush()
        # Все символы, кроме забоя, добавляются в конец буфера и эхо-копируются
        else:
            input_buffer.append(input_char)
            sys.stdout.write(input_char.decode())
            sys.stdout.flush()

    clear_line()
    return b''.join(input_buffer).decode()