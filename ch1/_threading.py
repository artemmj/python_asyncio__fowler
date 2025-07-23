import threading

def hello_from_thread():
    print(f'Привет от потока {threading.current_thread()}!')

hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

hello_thread2 = threading.Thread(target=hello_from_thread)
hello_thread2.start()

total_threads = threading.active_count()
print(f'В данный момент Python выполняет {total_threads} поток(ов)')

thread_name = threading.current_thread().name
print(f'Имя текущего потока {thread_name}')

hello_thread.join()
hello_thread2.join()
