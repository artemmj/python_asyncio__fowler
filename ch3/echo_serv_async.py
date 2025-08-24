import asyncio
import logging
import socket
import signal
from asyncio import AbstractEventLoop
from typing import List


async def echo(connection: socket, loop: AbstractEventLoop):
    try:
        # В бесконечном цикле ожидаем данные от клиента
        while data := await loop.sock_recv(connection, 1024):
            print(f'Получены данные: {data}')
            if data == b'exit\r\n':
                raise Exception('Ошибка сети!')
            # Получив данные, отправляем обратно клиенту
            await loop.sock_sendall(connection, data)
    except Exception as exc:
        logging.exception(exc)
    finally:
        connection.close()


echo_tasks = []
async def connection_listener(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получено сообщение от {address}')
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # Здесь мы ожидаем истечения таймаута
            pass


async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    print('Сервер работает и ждет подключений...')

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    # Запускаем сопрограмму прослушивания порта на предмет подключений
    await connection_listener(server_socket, loop)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
