import asyncio
from asyncio import Queue, PriorityQueue
from dataclasses import dataclass, field
from typing import Tuple


@dataclass(order=True)
class WorkItem:
    priority: int
    order: int
    data: str = field(compare=False)


async def worker(queue: Queue):
    while not queue.empty():
        work_item: WorkItem = await queue.get()
        print(f'Обрабатывается элемент {work_item}')
        queue.task_done()


async def main():
    priority_queue = PriorityQueue()
    work_items = [
        WorkItem(1, 1, 'High priority'),
        WorkItem(3, 1, 'Lowest priority'),
        WorkItem(3, 2, 'Lowest priority second'),
        WorkItem(3, 3, 'Lowest priority third'),
        WorkItem(2, 1, 'Medium priority'),
    ]
    for work in work_items:
        priority_queue.put_nowait(work)
    worker_task = asyncio.create_task(worker(priority_queue))
    await asyncio.gather(priority_queue.join(), worker_task)


if __name__ == '__main__':
    asyncio.run(main())
