from typing import Dict, List
import asyncpg
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()
DB_KEY = 'database'


async def create_database_pool(app: Application):
    print('Создается пул подключений...')
    pool: asyncpg.Pool = await asyncpg.create_pool(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password',
        database='products',
        min_size=6,
        max_size=6,
    )
    app[DB_KEY] = pool
    print('Пул подключений успешно создан...')


async def destroy_database_pool(app: Application):
    print('Уничтожается пул подключений.')
    pool: asyncpg.Pool = app[DB_KEY]
    await pool.close()


@routes.get('/brands')
async def brands(request: Request) -> Response:
    connection: asyncpg.Pool = request.app[DB_KEY]
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[asyncpg.Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)


@routes.get('/products/{id}')
async def get_product(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        product_id = int(str_id)
        query = \
            """
            SELECT
            product_id, product_name, brand_id
            FROM product
            WHERE product_id = $1
            """
        connection: asyncpg.Pool = request.app[DB_KEY]
        result: asyncpg.Record = await connection.fetchrow(query, product_id)
        if result is not None:
            return web.json_response(dict(result))
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest() 


app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app, port=8000)
