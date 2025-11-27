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

    if comprehension_time <= loop_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")

    print(f"{comprehension_time: .6f} vs {loop_time: .6f}")


if __name__ == "__main__":
    main()
