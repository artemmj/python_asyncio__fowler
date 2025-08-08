import asyncio
import functools
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Dict, List

map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    """Объединяет два словаря, складывая кол-во каждого ключа."""
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    """Подсчитывает количество каждого слова в чанке данных."""
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Завершено операций отображения: {map_progress.value}/{total_partitions}')
        await asyncio.sleep(1)


async def main(partition_size: int):
    global map_progress

    with open('./ch6/all-1gram', encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value('i', 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress,)) as pool:
            start_time = time.time()

            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))

            counters = await asyncio.gather(*tasks)

            await reporter

            final_result = functools.reduce(merge_dictionaries, counters)
            print(f'Aardvark встречается {final_result["Aardvark"]} раз.')
            print(f'Время MapReduce: {(time.time() - start_time):.4f} секунд')


if __name__ == '__main__':
    asyncio.run(main(50_000))
