import threading
import time

def print_fib(number: int) -> None:
    def fib(n: int):
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    print(f'fib({number}) равно {fib(number)}')

# def fibs_no_threading():
#     print_fib(40)
#     print_fib(41)
# start = time.time()
# fibs_no_threading()
# end = time.time()
# print(f'Время работы {end - start:.4f} с.')

def fibs_with_threads():
    thread_1 = threading.Thread(target=print_fib, args=(40,))
    thread_2 = threading.Thread(target=print_fib, args=(41,))
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
start = time.time()
fibs_with_threads()
end = time.time()
print(f'Время работы {end - start:.4f} с.')
