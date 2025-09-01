import asyncio
from asyncio import Queue
from random import randrange
from typing import List


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: List[Product]):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    while True:
        # Выбираем покупателя, если в очереди кто-то есть
        customer: Customer = await queue.get()
        print(f'Кассир {cashier_number} обслуживает покупателя {customer.customer_id}')

        # Обрабатываем каждый товар, купленный покупателем
        for product in customer.products:
            print(f"Кассир {cashier_number} обслуживает покупателя {customer.customer_id}: {product.name}")
            await asyncio.sleep(product.checkout_time)

        print(f'>> Кассир {cashier_number} закончил обслуживать покупателя {customer.customer_id}')
        queue.task_done()


def generate_customer(customer_id: int) -> Customer:
    """Сгенерировать случайного покупателя."""
    all_products = [
        Product('пиво', 2),
        Product('бананы', 2),
        Product('колбаса', 2),
        Product('подгузники', 2),
    ]
    products = [all_products[randrange(len(all_products))] for _ in range(randrange(10))]
    return Customer(customer_id, products)


async def customer_generator(queue: Queue):
    """Генерировать несколько случайных покупателей в секунду."""
    customer_count = 0
    while True:
        customers = [
            generate_customer(i)
            for i in range(customer_count + 1, customer_count + randrange(1, 6))
        ]
        for customer in customers:
            print('> Ожидаю возможности поставить покупателя в очередь...')
            await queue.put(customer)
            print('Покупатель поставлен в очередь!')
            customer_count += 1
            await asyncio.sleep(1)


async def main():
    customer_queue = Queue(5)

    # Создать 10 покупателей со случайным набором товаров
    # for i in range(1, 11):
    #     products = [all_products[randrange(len(all_products))] for _ in range(randrange(5, 10))]
    #     customer_queue.put_nowait(Customer(i, products))
    # await asyncio.gather(customer_queue.join(), *cashiers)


    customer_producer = asyncio.create_task(customer_generator(customer_queue))
    # Создать трех «кассиров», т. е. задач-исполнителей, обслуживающих
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i)) for i in range(1, 8)]
    await asyncio.gather(customer_producer, *cashiers)


if __name__ == '__main__':
    asyncio.run(main())
