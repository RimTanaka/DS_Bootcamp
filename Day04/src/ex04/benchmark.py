#!/usr/bin/python3

import timeit
import random
from collections import Counter


def get_random_list() -> list:
    return [random.randrange(10) for _ in range(1_000_000)]


def get_dict_with_loop(lst: list) -> dict:
    result = {}
    for number in lst:
        result[number] = result.get(number, 0) + 1
    return result


def get_dict_with_counter(lst: list) -> dict:
    return dict(Counter(lst))


def get_top_with_loop(d: dict) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:10])


def get_top_with_counter(d: dict) -> dict:
    return dict(Counter(d).most_common(10))


def main():
    lst = get_random_list()

    time_dict_loop = timeit.timeit(
        stmt="get_dict_with_loop(lst)",
        globals={"lst": lst, "get_dict_with_loop": get_dict_with_loop},
        number=1,
    )
    time_top_loop = timeit.timeit(
        stmt="get_top_with_loop(get_dict_with_loop(lst))",
        globals={"lst": lst, "get_top_with_loop": get_top_with_loop, "get_dict_with_loop": get_dict_with_loop},
        number=1,
    )

    time_dict_counter = timeit.timeit(
        stmt="get_dict_with_counter(lst)",
        globals={"lst": lst, "get_dict_with_counter": get_dict_with_counter},
        number=1,
    )
    time_top_counter = timeit.timeit(
        stmt="get_top_with_counter(lst)",
        globals={"lst": lst, "get_top_with_counter": get_top_with_counter},
        number=1,
    )

    print(f"my function: {time_dict_loop: .7f}")
    print(f"Counter: {time_dict_counter: .7f}")
    print(f"my top: {time_top_loop: .7f}")
    print(f"Counter's top: {time_top_counter: .7f}")


if __name__ == "__main__":
    main()
