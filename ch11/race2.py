import asyncio


class MockSocket:
    def __init__(self):
        self.socket_closed = False

    async def send(self, msg: str):
        """Имитировать медленную отправку сообщения клиенту."""
        if self.socket_closed:
            raise Exception('Сокет закрыт!')
        print(f'Отправляется: {msg}')
        await asyncio.sleep(1)
        print(f'Отправлено: {msg}')

    def close(self):
        self.socket_closed = True


user_names_to_sockets = {
    'John': MockSocket(),
    'Terry': MockSocket(),
    'Graham': MockSocket(),
    'Eric': MockSocket(),
}


async def message_all_users():
    print('Создаются задачи отправки сообщений...')
    # Сначала создаем задачи отправки сообщений
    messages = [socket.send(f'Привет, {user}') for user, socket in user_names_to_sockets.items()]
    # Затем выполняем предложение await, приостанавливающее сопрограмму.
    # Это дает шанс выполниться сопрограмме user_ disconnect('Eric'), которая
    # закрывает сокет Эрика и удаляет его из словаря user_names_to_sockets.
    await asyncio.gather(*messages)


async def user_disconnect(username: str):
    """Отключить пользователя и удалить его из памяти приложения."""
    socket = user_names_to_sockets.pop(username)
    print(f'{username} отключен!')
    socket.close()


async def main():
    await asyncio.gather(message_all_users(), user_disconnect('Eric'))


if __name__ == '__main__':
    asyncio.run(main())
