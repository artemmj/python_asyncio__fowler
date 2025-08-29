import asyncpg
from fastapi import FastAPI


app = FastAPI()
DATABASE_URL = 'postgresql://postgres:password@127.0.0.1/products'


@app.get("/brands")
async def brands():
    pool: asyncpg.Pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password',
        database='products',
        min_size=6,
        max_size=6,
    )
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results = await pool.fetch(brand_query)
    result_as_dict = [dict(brand) for brand in results]
    pool.close()
    return result_as_dict


# TODO
