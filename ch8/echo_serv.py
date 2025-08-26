import asyncio
import logging
from asyncio import StreamReader, StreamWriter
from typing import List


class ServerState:
    def __init__(self):
        self._writers: List[StreamWriter] = []

    async def add_client(self, reader: StreamReader, writer: StreamWriter):
        """Добавить клиента в состояние сервера и создать задачу эхо-копирования."""
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: StreamWriter):
        """
        После подключения нового клиента сообщить ему, сколько клиентов
        подключено, и уведомить остальных о новом пользователе.
        """
        writer.write(
            f'Добро пожаловать! Число подключенных пользователей: {len(self._writers)}.\n'.encode()
        )
        await writer.drain()
        await self._notify_all('Подключился новый пользователь.\n')

    async def _echo(self, reader: StreamReader, writer: StreamWriter):
        """
        Обработать эхо-копирование ввода при отключении клиента
        и уведомить остальных пользователей об отключении.
        """
        try:
            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(
                f'Клиент отключился! Осталось пользователей: {len(self._writers)}.\n'
            )
        except Exception as exc:
            logging.exception('Ошибка чтения данных от клиента.', exc_info=exc)
            self._writers.remove(writer)

    async def _notify_all(self, message: str):
        """
        Вспомогательный метод для отправки сообщения всем остальным пользователям.
        Если отправить сообщение не удалось, удалить данного пользователя.
        """
        for writer in self._writers:
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError as exc:
                logging.exception('Ошибка записи данных клиенту.', exc_info=exc)
                self._writers.remove(writer)


async def main():
    server_state = ServerState()

    async def client_connected(reader: StreamReader, writer: StreamWriter) -> None:
        """При подключении нового клиента добавить его в состояние сервера."""
        await server_state.add_client(reader, writer)

    # Запустить сервер и обслуживать запросы бесконечно
    server = await asyncio.start_server(client_connected, '127.0.0.1', 8000)
    print('Сервер запущен...')

    async with server:
        await server.serve_forever()


asyncio.run(main())
