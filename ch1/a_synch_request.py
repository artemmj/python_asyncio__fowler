import threading
import time
import requests


def read_status_code() -> None:
    response = requests.get('http://example.com')
    print(response.status_code)


def main():
    print('Начинаю синхронное выполнение запросов...')
    start = time.time()
    read_status_code()
    read_status_code()
    end = time.time()
    print(f'Синхронное выполнение заняло {end - start:.4f} с.', end='\n\n')

    print('Начинаю многопоточное выполнение запросов...')
    th1 = threading.Thread(target=read_status_code)
    th2 = threading.Thread(target=read_status_code)
    start = time.time()
    th1.start()
    th2.start()
    print('Все потоки работают')
    th1.join()
    th2.join()
    end = time.time()
    print(f'Многопоточное выполнение заняло {end - start:.4f} с.')


if __name__ == '__main__':
    main()
