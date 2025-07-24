import asyncio

from utils import delay

async def add_one(number: int) -> int:
    return number + 1

async def hello_world_message() -> str:
    await delay(1)
    return 'Hello world!'

async def main() -> None:
    message = await hello_world_message()
    one_p_one = await add_one(1)
    print(message)
    print(one_p_one)

asyncio.run(main())
