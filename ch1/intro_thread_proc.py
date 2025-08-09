import multiprocessing
import os
import threading


def hello_from_thread():
    print(f'Исполняется поток: {threading.current_thread()} ({os.getpid()})')
    print(f'... python выполняет {threading.active_count()} поток(ов)\r\n')


def hello_from_process():
    print(f'Исполняется дочерний процесс c pid: {os.getpid()} ({threading.current_thread()})')


def main():
    print(f'Идентификатор главного Python-процесса: {os.getpid()} ({threading.current_thread().name})\r\n')

    hello_thread1 = threading.Thread(target=hello_from_thread)
    hello_thread1.start()
    hello_thread2 = threading.Thread(target=hello_from_thread)
    hello_thread2.start()
    hello_thread1.join()
    hello_thread2.join()

    hello_process1 = multiprocessing.Process(target=hello_from_process)
    hello_process2 = multiprocessing.Process(target=hello_from_process)
    hello_process1.start()
    hello_process2.start()
    hello_process1.join()
    hello_process2.join()

    print(f'\r\nВ данный момент Python выполняет {threading.active_count()} поток(ов)')


if __name__ == '__main__':
    main()
