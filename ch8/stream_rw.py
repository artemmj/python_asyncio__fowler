import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    """Читать и декодировать строку, пока не кончатся символы."""
    while response := await stream_reader.readline():
        yield response.decode()


async def main():
    host = 'www.example.com'
    reqst = f'GET / HTTP/1.1\r\n' \
            f'Connection: close\r\n' \
            f'Host: {host}\r\n\r\n'
    # Открыть подключение, попутно создаем экземпляры StreamReader и StreamWriter
    stream_reader, stream_writer = await asyncio.open_connection(host, 80)

    try:
        stream_writer.write(reqst.encode())  # Записать http-запрос
        await stream_writer.drain()          # и опустошить буфер писателя
        # Читать строки и сохранять их в списке
        responses = [response async for response in read_until_empty(stream_reader)]
        print(''.join(responses))
    finally:
        stream_writer.close()              # Закрыть писатель
        await stream_writer.wait_closed()  # и ждать завершения закрытия


asyncio.run(main())
