#!/usr/bin/python3

import timeit
import sys

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


def benchmark(function_name, repetitions):
    """
    Функция для замера времени выполнения заданной функции.

    :param function_name: Выбор метода loop/map/lisit/filter.
    :param repetitions: Количество повторений.
    :return: Время затраченное на работу метода.
    """

    if function_name == "loop":
        time = timeit.timeit(
            stmt="get_gmails_with_loop(emails)",
            setup="from __main__ import get_gmails_with_loop, emails",
            globals=globals(),
            number=repetitions
        )
    elif function_name == "list_comprehension":
        time = timeit.timeit(
            stmt="get_gmails_with_comprehension(emails)",
            setup="from __main__ import get_gmails_with_comprehension, emails",
            globals=globals(),
            number=repetitions
        )
    elif function_name == "map":
        time = timeit.timeit(
            stmt="get_gmails_with_map(emails)",
            setup="from __main__ import get_gmails_with_map, emails",
            globals=globals(),
            number=repetitions
        )
    elif function_name == "filter":
        time = timeit.timeit(
            stmt="get_gmails_with_filter(emails)",
            setup="from __main__ import get_gmails_with_filter, emails",
            globals=globals(),
            number=repetitions
        )
    else:
        raise ValueError(f"Unknown function name: {function_name}")
    return time

def main():
    if len(sys.argv) != 3:
        print("Usage: ./benchmark.py <function_name> <repetitions>")
        sys.exit(1)

    name = sys.argv[1]
    try:
        repetitions = int(sys.argv[2])
    except ValueError:
        print("<repetitions> must be an integer")
        sys.exit(1)

    try:
        execution_time = benchmark(name, repetitions)
        print(f"{execution_time: .6f}")
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
