import asyncio
from asyncio import Transport, Future, AbstractEventLoop
from typing import Optional


class HTTPGetClientProtocol(asyncio.Protocol):
    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    async def get_response(self):
        """
        Ждать внутренний будущий объект, пока не будет получен ответ от сервера.
        """
        return await self._future

    def connection_made(self, transport: Transport):
        """
        После того как подключение установлено, использовать транспорт для отправки запроса.
        """
        print(f'Создано подключение к {self._host}')
        self._transport = transport
        self._transport.write(
            f'GET / HTTP/1.1\r\n' \
            f'Connection: close\r\n' \
            f'Host: {self._host}\r\n\r\n'.encode()
        )

    def data_received(self, data):
        """Получив данные, сохранить их во внутреннем буфере."""
        print('Данные получены...')
        self._response_buffer += (data[:200] + b'\n.........')

    def eof_received(self) -> Optional[bool]:
        """
        После закрытия подключения завершить будущий объект, скопировав в него данные из буфера.
        """
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """
        Если подключение было закрыто без ошибок, не делать ничего;
        иначе завершить будущий объект исключением
        """
        if exc is None:
            print('Подключение закрыто... Ошибок нет.')
        else:
            self._future.set_exception(exc)


async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    # def protocol_factory():
    #     return HTTPGetClientProtocol(host, loop)
    _, protocol = await loop.create_connection(lambda: HTTPGetClientProtocol(host, loop), host=host, port=port)
    return await protocol.get_response()


async def main():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)


asyncio.run(main())
