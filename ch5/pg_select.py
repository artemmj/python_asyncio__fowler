import asyncio
import asyncpg

from utils import async_timed
from _sql_commands import product_query


async def query_product(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_products_synchronously(pool: asyncpg.Pool, queries):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


async def main():
    async with asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='artemmj',
        database='products',
        password='Cher86',
        min_size=6,
        max_size=6,
    ) as pool:
        await query_products_synchronously(pool, 50000)
        await query_products_concurrently(pool, 50000)


asyncio.run(main())
