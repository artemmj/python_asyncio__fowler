from multiprocessing import Process, Value, Array


def inc_value(shared_int: Value):
    # with shared_int.get_lock()
    shared_int.get_lock().acquire()
    shared_int.value += 1
    shared_int.get_lock().release()


def inc_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


if __name__ == '__main__':
    for _ in range(100):
        integer = Value('i', 0)
        # integer_array = Array('i', [0, 0])

        procs = [
            Process(target=inc_value, args=(integer,)),
            Process(target=inc_value, args=(integer,)),
            # Process(target=inc_array, args=(integer_array,))
        ]

        [p.start() for p in procs]
        [p.join() for p in procs]
        print(integer.value)
        assert integer.value == 2
        # print(integer_array[:])
