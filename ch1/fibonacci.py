import multiprocessing
import threading
import time


def slow_calc_fib(number: int) -> None:
    """Медленная функция для рекурсивного вычисления факториала числа."""
    def fib(n: int):
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    print(f'fib({number}) равно {fib(number)}')


def main():
    print('Считаю числа синхронно...')
    start = time.time()
    slow_calc_fib(38)
    slow_calc_fib(39)
    end = time.time()
    print(f'Время работы {end - start:.2f} с.\r\n')

    print('Считаю числа в отдельных потоках...')
    start = time.time()
    thread_1 = threading.Thread(target=slow_calc_fib, args=(38,))
    thread_2 = threading.Thread(target=slow_calc_fib, args=(39,))
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    end = time.time()
    print(f'Время работы {end - start:.2f} с.\r\n')

    print('Считаю числа в отдельных процессах...')
    start = time.time()
    process_1 = multiprocessing.Process(target=slow_calc_fib, args=(38,))
    process_2 = multiprocessing.Process(target=slow_calc_fib, args=(39,))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()
    end = time.time()
    print(f'Время работы {end - start:.2f} с.')


if __name__ == '__main__':
    main()
