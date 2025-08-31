import asyncio
from asyncio import Condition


async def do_work(condition: Condition):
    while True:
        print('do_work(): Ожидаю блокировки условия...')
        # Ждать возможности захватить блокировку условия; после захвата освободить блокировку
        async with condition:
            print('do_work(): Блокировка захвачена, освобождаю и жду выполнения условия...')
            # Ждать события; когда оно произойдет, заново захватить блокировку условия
            await condition.wait()
            print('do_work(): Условие выполнено, вновь захватываю блокировку и начинаю работать...')
            await asyncio.sleep(1)
        # После выхода из блока async with освободить блокировку условия
        print('do_work(): Работа закончена, блокировка освобождена...')


async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print('fire_event(): Перед уведомлением, захватываю блокировку условия...')
        async with condition:
            print('fire_event(): Блокировка захвачена, уведомляю всех исполнителей.')
            condition.notify_all()  # уведомить все задачи о событии
        print('fire_event(): Исполнители уведомлены, освобождаю блокировку.')


async def main():
    condition = Condition()
    asyncio.create_task(fire_event(condition))
    await asyncio.gather(do_work(condition), do_work(condition))


if __name__ == '__main__':
    asyncio.run(main())
