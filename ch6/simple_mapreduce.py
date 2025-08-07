import functools
from typing import Dict


def map_frequency(text: str) -> Dict[str, int]:
    """Подсчитывает количество каждого слова в предложении."""
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    """Объединяет два словаря, складывая кол-во каждого ключа."""
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged

lines = ["I know what I know",
        "I know that I know",
        "I don't know much",
        "They don't know much"]

mapped_results = [map_frequency(line) for line in lines]
for result in mapped_results:
    print(result)

print()
print(functools.reduce(merge_dictionaries, mapped_results))
