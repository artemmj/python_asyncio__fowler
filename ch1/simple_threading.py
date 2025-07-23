import os
import threading

print(f'Исполняется Python-процесс с идентификатором: {os.getpid()}')

total_threads = threading.active_count()
print(f'В данный момент Python исполняет {total_threads} поток(ов)')

thread_name = threading.current_thread().name
print(f'Имя текущего потока {thread_name}')
