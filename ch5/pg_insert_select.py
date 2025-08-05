import asyncpg
import asyncio

from asyncpg import Record
from typing import List


async def main():
    pgconn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres',
    )
    print(f'БД Postgres успешно подключена. Версия : {pgconn.get_server_version().major}')

    await pgconn.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await pgconn.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await pgconn.fetch(brand_query)

    for row in results:
        print(f'id: {row["brand_id"]}, name: {row["brand_name"]}')

    await pgconn.close()


asyncio.run(main())
