import asyncio
from threading import RLock
from typing import List


class IntListThreadsafe:
    """
    Потокобезопасный класс списка целых чисел. Имеется метод
    поиска всех элементов с указанным значением и метод замены.
    Оба захватывают блокировку, поэтому нужно использовать RLock. 
    """
    def __init__(self, wrapped_list: List[int]):
        self._lock = RLock()  # блокировка для предотвращения гонки (Lock не подойдет)
        self._inner_list = wrapped_list

    def indices_of(self, to_find: int) -> List[int]:
        """Метод возвращает индексы вхождений элемента в списке."""
        with self._lock:
            enumerator = enumerate(self._inner_list)
            return [index for index, value in enumerator if value == to_find]

    def find_and_replace(self, to_replace: int, replace_with: int) -> None:
        with self._lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self._inner_list[index] = replace_with


async def main():
    threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
    threadsafe_list.find_and_replace(1, 2)
    print(threadsafe_list._inner_list)


asyncio.run(main())
