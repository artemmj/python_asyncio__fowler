import asyncio
import socket
from asyncio import AbstractEventLoop

async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен запрос на подключение от {address}')
        # После запроса на подключение, создаем задачу echo, ождидающую данные от клиента
        asyncio.create_task(echo(connection, loop))

async def echo(connection: socket, loop: AbstractEventLoop):
    # В бесконечном цикле ожидаем данные от клиента
    while data := await loop.sock_recv(connection, 1024):
        
        # Получив данные, отправляем обратно клиенту
        await loop.sock_sendall(connection, data)

async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    print('Сервер работает и ждет подключений...')

    # Запускаем сопрограмму прослушивания порта на предмет подключений
    await listen_for_connection(server_socket, asyncio.get_event_loop())

asyncio.run(main())
