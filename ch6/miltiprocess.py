import asyncio
import time
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Pool


def say_hello(name: str) -> str:
    return f'Привет, {name}'


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f'Закончен подсчет до {count_to} за время {end-start}')
    return counter


async def main():
    start = time.time()
    # Создаем процесы под выполнения каждой фукнции
    to_one_hundred_million = Process(target=count, args=(100000000,))
    to_two_hundred_million = Process(target=count, args=(200000000,))
    # Запускаем процессы, метод возвращает управление немедленно
    to_one_hundred_million.start()
    to_two_hundred_million.start()
    # Ждем завершения процессов, метод блокирует выполнение, пока процесс не завершится
    to_one_hundred_million.join()
    to_two_hundred_million.join()
    end = time.time()
    print(f'Время работы {end - start}')

    # Пул процессов
    with Pool() as process_pool:
        # Выполнить фукнции с разным аргументами в отдельных процессах
        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))
        hi_john = process_pool.apply_async(say_hello, args=('John',))
        print(hi_jeff.get())
        print(hi_john.get())

    # Использование ProcessPoolExecutor
    with ProcessPoolExecutor() as process_pool:
        numbers = [10, 30, 100_000_000, 50, 220]
        for result in process_pool.map(count, numbers):
            print(result)

    # Исполнитель пула процессов в сочетании с asyncio
    with ProcessPoolExecutor() as process_pool:
        # Получить текущий цикл событий
        loop = asyncio.get_running_loop()
        numbers = [10, 30, 100_000_000, 50, 220]
        # Сформировать все обращения к пулу процессов, поместив их в список
        calls = [partial(count, num) for num in numbers]
        call_coros = []
        # Вызовы можно передать исполнителю - вызывая loop.run_in_executor для каждого и
        # сохраняя полученные в ответ объекты, допускающие ожидание, в списке call_coros
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))
        # Затем передаем этот список в .gather и ждем завершения всех вызовов
        results = await asyncio.gather(*call_coros)
        for res in results:
            print(res)


if __name__ == '__main__':
    asyncio.run(main())
