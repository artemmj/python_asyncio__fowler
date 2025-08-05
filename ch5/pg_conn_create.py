import asyncio
import asyncpg
from typing import List, Tuple, Union
from random import sample

from sql_commands import (
    CREATE_BRAND_TABLE,
    CREATE_PRODUCT_TABLE,
    CREATE_PRODUCT_COLOR_TABLE,
    CREATE_PRODUCT_SIZE_TABLE,
    CREATE_SKU_TABLE,
    # COLOR_INSERT,
    # SIZE_INSERT,
)


def load_common_words() -> List[str]:
    """Загружает список рандомных слов из файла в память."""
    with open('./ch5/common_words.txt') as ifile:
        return ifile.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, ]]]:
    """Генерирует на основе переданных слов рандомно 100 кортежей."""
    return [(words[index],) for index in sample(range(1000), 100)]


async def insert_brands(common_words, connection) -> int:
    """Вставляет сгененированные слова в таблицу."""
    brands = generate_brand_names(common_words)
    return await connection.executemany("INSERT INTO brand VALUES(DEFAULT, $1)", brands)


async def main():
    pgconn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='postgres',
    )
    version = pgconn.get_server_version()
    print(f'Подключено! Версия Postgres: {version}')

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_SKU_TABLE,
        # COLOR_INSERT,
        # SIZE_INSERT,
    ]
    for statement in statements:
        status = await pgconn.execute(statement)
        print(status)

    common_words = load_common_words()
    await insert_brands(common_words, pgconn)

    await pgconn.close()


asyncio.run(main())
