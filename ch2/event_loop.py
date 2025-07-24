import asyncio

from utils import delay

def call_later():
    print('Меня вызовут в ближайшем будущем')

async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

asyncio.run(main())

# loop = asyncio.new_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()
