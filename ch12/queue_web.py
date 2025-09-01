import asyncio
from asyncio import Queue, Task
from typing import List
from random import randrange
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()

QUEUE_KEY = 'order_queue'
TASKS_KEY = 'order_tasks'


async def process_order_worker(worker_id: int, queue: Queue):
    """Выбрать заказ из очереди и обработать его."""
    while True:
        print(f'Worker ({worker_id}): ожидание заказа...')
        order = await queue.get()
        print(f'Worker ({worker_id}): обрабатывается заказ ({order})')
        await asyncio.sleep(order)
        print(f'Worker ({worker_id}): заказ ({order}) обработан')
        queue.task_done()


async def create_queue(app: Application):
    """Создать очередь на 10 элементов и 5 задач-исполнителей."""
    print('Создание очереди заказов и задач.')
    queue: Queue = asyncio.Queue(10)
    app[QUEUE_KEY] = queue
    app[TASKS_KEY] = [asyncio.create_task(process_order_worker(i, queue)) for i in range(1, 6)]


async def destroy_queue(app: Application):
    """Ждать завершения работающих задач."""
    order_tasks: List[Task] = app[TASKS_KEY]
    queue: Queue = app[QUEUE_KEY]
    print('Ожидание завершения исполнителей в очереди...')
    try:
        await asyncio.wait_for(queue.join(), timeout=10)
    finally:
        print('Обработка всех заказов завершена, отменяются задачи-исполнители...')
        [task.cancel() for task in order_tasks]


@routes.post('/order')
async def place_order(request: Request) -> Response:
    order_queue = app[QUEUE_KEY]
    # Поместить заказ в очередь и ответить пользователю немедленно
    await order_queue.put(randrange(1, 6))
    return Response(body='Order placed!')


app = web.Application()
app.on_startup.append(create_queue)
app.on_shutdown.append(destroy_queue)
app.add_routes(routes)
web.run_app(app, port=9000)
