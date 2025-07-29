import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8001)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()
print('Сервер запущен и ждет клиентов')

selector.register(server_socket, selectors.EVENT_READ)

while True:
    # Создать селектор с таймаутом 1 сек
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    # Если ничего не происходит, сообщить об этом
    if len(events) == 0:
        print('Событий нет, ожидаю...')

    for event, _ in events:
        # Получить сокет, для которого произошло событие (хранится в fileobj)
        event_socket = event.fileobj

        # Если событие произошло с серверным сокетом, это попытка подключения
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"Получен запрос на подключение от {address}")
            # Зарегать клиент, подключившийся к серверу
            selector.register(connection, selectors.EVENT_READ)
        # Если не с серверным, получить данные от клиента и отправить обратно
        else:
            data = event_socket.recv(1024)
            print(f"Полученые данные от клиента: {data}")
            event_socket.send(data)
