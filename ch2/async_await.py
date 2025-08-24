import asyncio

from utils import delay


async def add_one(number: int) -> int:
    return number + 1


async def print_hi() -> str:
    await delay(1)
    return 'Hello world!'

# Код ведет себя как последовательный

async def main() -> None:
    one_p_one = await add_one(1)
    # main() приостанавливается, до выполнения await add_one()
    message = await print_hi()
    # main() приостанавливается, до выполнения await print_hi()

    print(f'add_one(1): {one_p_one}')
    print(f'print_hi(): {message}')


asyncio.run(main())
