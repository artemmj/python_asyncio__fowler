import sys
import asyncio
from asyncio import StreamReader

from _delay_func import delay


async def create_stdin_reader() -> StreamReader:
    """Функция создает и возвращает асинхронный читатель стандартного ввода."""
    # Создаем объект StreamReader который используется
    # для асинхронного чтения стандартного ввода
    stream_reader = asyncio.StreamReader()
    # Объект передается протоколу потокового читателя
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    # Затем вызывается сопрограмма connect_read_pipe, ей
    # передается фабрика протоколов, реализованная в виде
    # лямбда-функции, которая возвращает созданный ранее протокол.
    # Также ей передается sys.stdin, который соединяется
    # с нашим протоколом потокового читателя.
    transport, _protocol = await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    print(protocol is _protocol)  # True
    return stream_reader


async def main():
    # Работать не будет
    # while True:
    #     delay_time = input('Введи время сна: ')
    #     asyncio.create_task(delay(int(delay_time)))

    # Создаем асинхронный читатель стандартного ввода
    stdin_reader = await create_stdin_reader()

    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))


if __name__ == '__main__':
    asyncio.run(main())
