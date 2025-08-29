import asyncio
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute


class UserCounter(WebSocketEndpoint):
    encoding = 'text'
    sockets = []

    async def on_connect(self, websocket):
        """
        Когда клиент подключается, добавить его список
        сокетов и сообщить остальным новое значение счетчика.
        """
        await websocket.accept()
        UserCounter.sockets.append(websocket)
        await self._send_count()

    async def on_disconnect(self, websocket, close_code):
        """
        Когда клиент отключается, удалить его из списка
        и сообщить остальным новое значение счетчика.
        """
        UserCounter.sockets.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket, data):
        pass

    async def _send_count(self):
        """
        Сообщить всем клиентам, сколько пользователей сейчас
        подключено. Если во время отправки сообщения возникнет
        исключение, удалить соответствующий клиент из списка.
        """
        if len(UserCounter.sockets) > 0:
            count_str = str(len(UserCounter.sockets))
            task_to_socket = {asyncio.create_task(websocket.send_text(count_str)): websocket for websocket in UserCounter.sockets}

            done, pending = await asyncio.wait(task_to_socket)
            for task in done:
                if task.exception() is not None:
                    if task_to_socket[task] in UserCounter.sockets:
                        UserCounter.sockets.remove(task_to_socket[task])


app = Starlette(routes=[WebSocketRoute('/counter', UserCounter)])
