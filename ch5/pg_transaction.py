import asyncio
import asyncpg
import logging
from asyncpg.transaction import Transaction


async def make_simple_transaction(conn: asyncpg.Connection):
    """Пример применения простой транзакции."""
    try:
        async with conn.transaction():
            await conn.execute("INSERT INTO brand VALUES(9999, 'brand_1')")
            # await conn.execute("INSERT INTO brand VALUES(9999, 'broke_brand')")
    except Exception:
        logging.exception('Ошибка выполнения транзакции.')
    finally:
        brands = await conn.fetch("""SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'""")
        print(f'Результат запроса: {brands}')


async def make_nested_transaction(conn: asyncpg.Connection):
    """Пример вложенной транзакции."""
    async with conn.transaction():
        await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")
        try:
            async with conn.transaction():
                await conn.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as exc:
            logging.warning('Ошибка при вставке цвета товара игнорируется', exc_info=exc)


async def manual_op_transaction(conn: asyncpg.Connection):
    """Пример ручного управления транзакциями."""
    transaction: Transaction = conn.transaction()
    await transaction.start()
    try:
        await conn.execute("INSERT INTO brand VALUES(9999, 'brand_1')")
        await conn.execute("INSERT INTO brand VALUES(9998, 'brand_2')")
    except asyncpg.PostgresError as exc:
        logging.error('Ошибка! Откат транзакции.', exc_info=exc)
        await transaction.rollback()
    else:
        logging.info('Ошибки нет. Фиксация транзакции.')
        await transaction.commit()

    brands = await conn.fetch("""SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'""")
    print(f'Результат запроса: {brands}')


async def main():
    conn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='artemmj',
        database='products',
        password='Cher86',
    )
    print(f'Подключено! Версия Postgres: {conn.get_server_version().major}')

    await make_simple_transaction(conn)
    await make_nested_transaction(conn)
    await manual_op_transaction(conn)

    await conn.close()


asyncio.run(main())
