#!/usr/bin/env python3
"""
Модуль для извлечения фин данных с Yahoo Finance по тикеру и выбранному полю.

Использует requests для получения данных и BeautifulSoup для парсинга HTML.
"""

import sys
import time
import requests
from bs4 import BeautifulSoup


def fetch_financial_data(ticker: str, field: str) -> list:
    """
    Получает финансовые данные компании с Yahoo Finance.

    Аргументы:
        ticker (str): Тикер компании (например, MSFT).

        field (str): Название поля таблицы (например, Total Revenue).

    Возвращает:
        list: Список значений для запрашиваемого поля.

    Исключения:
        ValueError: Если не удается найти запрашиваемое поле.
        requests.exceptions.RequestException: Если ошибка запроса к URL
    """
    url = f"https://finance.yahoo.com/quote/{ticker.upper()}/financials"
    print(f"Собираем данные с сайта: {url}")

    time.sleep(5)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0)\
        Gecko/20100101 Firefox/133.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as ex:
        raise requests.exceptions.RequestException(f"Error fetching URL: {url}"
                                                   ) from ex

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("div", {"class": "tableBody yf-9ft13"})
    if not table:
        raise ValueError("Financial data table not found on the page.")

    financial_data = {}

    for div in table.find_all("div", class_="row lv-0 yf-t22klz"):
        columns = div.find_all("div")
        data = [col.text.strip() for col in columns]

        if data[0] and len(data) > 1:
            name = data[0]
            values = data[1:] if len(data[1]) > 0 else data[2:]

            financial_data[name] = values

    if not financial_data.get(field):
        raise ValueError(f"Field '{field}' not found on the page.")

    # for i in financial_data:
    #     print(i)
    # print(" ")

    return financial_data[field]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./financial.py 'TICKER' 'FIELD'")
        sys.exit(1)

    ticker_find = sys.argv[1].strip()
    field_find = sys.argv[2].strip()

    try:
        result = fetch_financial_data(ticker_find, field_find)
        print(result)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
