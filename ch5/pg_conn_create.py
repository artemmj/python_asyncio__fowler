import asyncio
import asyncpg
from typing import List, Tuple, Union
from random import randint, sample

from _sql_commands import (
    CREATE_BRAND_TABLE,
    CREATE_PRODUCT_TABLE,
    CREATE_PRODUCT_COLOR_TABLE,
    CREATE_PRODUCT_SIZE_TABLE,
    CREATE_SKU_TABLE,
    COLOR_INSERT,
    SIZE_INSERT,
    product_query,
)


def load_common_words() -> List[str]:
    """Загружает список рандомных слов из файла в память."""
    with open('./ch5/_common_words.txt') as ifile:
        return ifile.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, ]]]:
    """Генерирует на основе переданных слов рандомно 100 кортежей."""
    return [(words[index],) for index in sample(range(1000), 100)]


async def insert_brands(common_words, connection) -> int:
    """Вставляет сгененированные слова в таблицу."""
    brands = generate_brand_names(common_words)
    return await connection.executemany("INSERT INTO brand VALUES(DEFAULT, $1)", brands)


def gen_products(
    common_words: List[str],
    brand_id_start: int,
    brand_id_end: int,
    products_to_create: int,
) -> List[Tuple[str, int]]:
    """Генерирует список товаров."""
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(1000), 10)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((' '.join(description), brand_id))
    return products


def gen_skus(product_id_start: int, product_id_end: int, skus_to_create: int) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def main():
    pgconn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='artemmj',
        database='products',
        password='Cher86',
    )
    version = pgconn.get_server_version()
    print(f'Подключено! Версия Postgres: {version}')

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_SKU_TABLE,
        COLOR_INSERT,
        SIZE_INSERT,
    ]
    for statement in statements:
        status = await pgconn.execute(statement)
        print(status)

    common_words = load_common_words()
    await insert_brands(common_words, pgconn)

    product_tuples = gen_products(common_words, 1, 100, 1000)
    await pgconn.executemany('INSERT INTO product VALUES(DEFAULT, $1, $2)', product_tuples)

    sku_tuples = gen_skus(1, 1000, 100000)
    await pgconn.executemany('INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)', sku_tuples)

    await pgconn.close()


asyncio.run(main())
