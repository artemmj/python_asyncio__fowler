import asyncio
import socket
from threading import Thread


class ClientEchoThread(Thread):
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client

    def run(self):
        print('Новое подключение, новый поток...')
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    # Если нет данных - возбудить исключение. это бывает, когда
                    # подключение было закрыто клиентом или остановлено сервером
                    raise BrokenPipeError('Исключение: Подключение закрыто...')
                print(f'Получено {data}, отправляю обратно...')
                self.client.sendall(data)
        except OSError as exc:
            # Выйти из метода run, если было исключение. Поток завершается
            print(f'Поток прерван исключением {exc}, производится остановка...')

    def close(self):
        if self.is_alive():
            # Разомкнуть подключение, если поток еще активен; поток
            # может быть неактивен, если клиент закрыл подключение
            self.client.sendall(bytes('Останавливаюсь...', encoding='utf-8'))
            # Разомкнуть подключение клиента, остановив чтение и запись
            self.client.shutdown(socket.SHUT_RDWR)


async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        connection_threads = []
        try:
            while True:
                connection, addr = server.accept()
                thread = ClientEchoThread(connection)
                connection_threads.append(thread)
                thread.start()
        except KeyboardInterrupt:
            print('Останавливаюсь...')
            [thread.close for thread in connection_threads]


if __name__ == '__main__':
    asyncio.run(main())
