#!/usr/bin/python3

import timeit
import sys
from functools import reduce

emails = [
             'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
             'anna@live.com', 'philipp@gmail.com'
         ] * 5


def get_gmails_with_loop(email_list):
    """
    Функция, использующая цикл для фильтрации Gmail.

    :param email_list: список почт
    :return: отфильтровованный список
    """
    gmails = []
    for email in email_list:
        if 'gmail.com' in email:
            gmails.append(email)
    return gmails


def get_gmails_with_map(email_list):
    """
    Функция, использующая map для фильтрации Gmail.

    :param email_list: список почт
    :return: отфильтровованный список
    """
    return map(lambda email: email if 'gmail.com' in email else None, email_list)


def get_gmails_with_comprehension(email_list):
    """
    Функция, использующая list comprehension для фильтрации Gmail.

    :param email_list: список почт
    :return: отфильтровованный список
    """
    return [email for email in email_list if 'gmail.com' in email]


def get_gmails_with_filter(email_list):
    """
    Функция, использующая Filter для фильтрации Gmail.

    :param email_list: список почт
    :return: отфильтровованный список
    """
    return filter(lambda email: 'gmail.com' in email, email_list)


def sum_of_squares_with_loop(n):
    """Функция, вычисляющая сумму квадратов с помощью цикла."""
    total = 0
    for i in range(1, n + 1):
        total = total + i * i
    return total


def add_squares(a, x):
    return a + x * x

def sum_of_squares_with_reduce(n):
    """Функция, вычисляющая сумму квадратов с помощью reduce."""
    return reduce(add_squares, range(1, n + 1))


def benchmark(function_name, repetitions, n: int = None):
    """
    Функция для замера времени выполнения заданной функции.

    :param function_name: Выбор метода loop/map/lisit/filter.
    :param repetitions: Количество повторений.
    :param n: Число которое будет возведено в квадрат
    :return: Время затраченное на работу метода.
    """

    if function_name == "loop":
        stmt = "get_gmails_with_loop(emails)" if n is None else "sum_of_squares_with_loop(n)"
    elif function_name == "list_comprehension":
        stmt = "get_gmails_with_comprehension(emails)"
    elif function_name == "map":
        stmt = "get_gmails_with_map(emails)"
    elif function_name == "filter":
        stmt = "get_gmails_with_filter(emails)"
    elif function_name == "reduce":
        stmt = "sum_of_squares_with_reduce(n)"
    else:
        raise ValueError(f"Unknown function name: {function_name}")

    if n is not None:
        globals()["n"] = n

    time = timeit.timeit(
        stmt=stmt,
        globals=globals(),
        number=repetitions
    )
    return time


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: ./benchmark.py <function_name> <repetitions> [<n>]")
        sys.exit(1)

    function_name = sys.argv[1]
    try:
        repetitions = int(sys.argv[2])
        n = int(sys.argv[3]) if len(sys.argv) == 4 else None
    except ValueError:
        print("<repetitions> and <n> must be integers")
        sys.exit(1)

    try:
        execution_time = benchmark(function_name, repetitions, n)
        print(f"{execution_time: .6f}")
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
