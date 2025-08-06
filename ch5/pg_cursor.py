import asyncio
from typing import Generator
import asyncpg


async def take(generator: Generator, to_take: int):
    """Собственный асинхронный генератор для использования async for."""
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count += 1
        yield item


async def main():
    conn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='artemmj',
        database='products',
        password='Cher86',
    )
    print(f'БД подключена, версия Postgres: {conn.get_server_version().major}')

    query = 'SELECT product_id, product_name FROM product'

    # Выборка всех элементов через курсор
    print('Выборка всех элементов через курсор')
    async with conn.transaction():
        async for product in conn.cursor(query, prefetch=50):
            print(product)

    # Перемещение по курсору
    print('\r\nПеремещение по курсору')
    async with conn.transaction():
        # Создать курсор для запроса
        cursor = await conn.cursor(query)
        # Сдвинуть курсор вперед на 500 записей
        await cursor.forward(500)
        # Получить следующие 100 записей
        products = await cursor.fetch(100)
        for product in products:
            print(product)

    # Получение заданного числа элементов с помощью собственного асинхронного генератора
    print('\r\nПолучение заданного числа элементов с помощью собственного асинхронного генератора')
    async with conn.transaction():
        product_generator = conn.cursor(query)
        async for product in take(product_generator, 5):
            print(product)
        print('Получены первые пять товаров!')

    await conn.close()


asyncio.run(main())
