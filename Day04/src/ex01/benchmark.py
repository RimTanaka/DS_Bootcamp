#!/usr/bin/python3

import timeit


emails = [
             'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
             'anna@live.com', 'philipp@gmail.com'
         ] * 5


def get_gmails_with_loop(email_list):
    """
    Функция, использующая цикл для фильтрации Gmail.
    """
    gmails = []
    for email in email_list:
        if 'gmail.com' in email:
            gmails.append(email)
    return gmails


def get_gmails_with_map(email_list):
    """
    Функция, использующая map для фильтрации Gmail.
    """
    return map(lambda email: email if 'gmail.com' in email else None, email_list)


def get_gmails_with_comprehension(email_list):
    """
    Функция, использующая list comprehension для фильтрации Gmail.
    """
    return [email for email in email_list if 'gmail.com' in email]


def main():
    repetitions = 90_000_000

    loop_time = timeit.timeit(
        stmt="get_gmails_with_loop(emails)",
        setup="from __main__ import get_gmails_with_loop, emails",
        number=repetitions
    )

    comprehension_time = timeit.timeit(
        stmt="get_gmails_with_comprehension(emails)",
        setup="from __main__ import get_gmails_with_comprehension, emails",
        number=repetitions
    )

    map_time = timeit.timeit(
        stmt="get_gmails_with_map(emails)",
        setup="from __main__ import get_gmails_with_map, emails",
        globals=globals(),
        number=repetitions
    )

    # print(f"map {list(get_gmails_with_map(emails))},\nlist {get_gmails_with_comprehension(emails)},\nloop {get_gmails_with_loop(emails)}")

    if map_time <= loop_time and map_time <= comprehension_time:
        print("it is better to use a map")
    elif comprehension_time <= loop_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")

    times = sorted([("loop", loop_time), ("list comprehension", comprehension_time), ("map", map_time)],
                   key=lambda x: x[1])
    for method, timing in times:
        print(f"{method}: {timing:.6f}")


if __name__ == "__main__":
    main()
