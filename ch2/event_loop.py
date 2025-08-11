import asyncio

from utils import delay


# Ручное создание цикла событий (asyncio.run())
# async def main():
#     await asyncio.sleep(1)
# loop = asyncio.new_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()


def call_later():
    print('Меня вызвали через call_soon()')


async def main():
    # Получить текущий цикла событий
    loop = asyncio.get_running_loop()
    # Метод принимает функцию и выполняет ее на следующей итерации цикла
    loop.call_soon(call_later)
    await delay(1)


asyncio.run(main(), debug=True)
