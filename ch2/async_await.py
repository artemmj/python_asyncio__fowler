import asyncio

async def add_one(number: int) -> int:
    return number + 1

async def main() -> None:
    one_p_one = await add_one(1)
    two_p_one = await add_one(2)
    print(one_p_one)
    print(two_p_one)

asyncio.run(main())
