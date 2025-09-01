import asyncio
from asyncio import Queue, LifoQueue
from dataclasses import dataclass, field
from typing import Tuple


@dataclass(order=True)
class WorkItem:
    priority: int
    order: int
    data: str = field(compare=False)


async def worker(queue: LifoQueue):
    while not queue.empty():
        # Выбрать элемент из очереди, или «вытолкнуть» его из стека
        work_item: WorkItem = await queue.get()
        print(f'Обрабатывается элемент {work_item}')
        queue.task_done()


async def main():
    lifo_q = LifoQueue()
    work_items = [
        WorkItem(3, 1, 'Lowest priority'),
        WorkItem(3, 2, 'Lowest priority second'),
        WorkItem(3, 3, 'Lowest priority third'),
        WorkItem(2, 4, 'Medium priority'),
        WorkItem(1, 5, 'High priority'),
    ]
    worker_task = asyncio.create_task(worker(lifo_q))
    for work in work_items:
        lifo_q.put_nowait(work)
    await asyncio.gather(lifo_q.join(), worker_task)


if __name__ == '__main__':
    asyncio.run(main())
