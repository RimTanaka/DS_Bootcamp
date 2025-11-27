"""
Модуль для анализа данных из файла links.csv с доступом к информации с IMDb.

Содержит класс Links, предоставляющий методы для извлечения
данных о режиссерах, бюджете, сборах, длительности фильмов
и расчета показателей, основанных на данных с IMDb.
"""

import csv
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Links:
    """
    Класс для анализа данных из файла links.csv.

    Атрибуты:
        path_to_the_file: Путь к файлу links.csv.

    Методы:
        get_imdb(movie_id:, list_of_fields): Получаем список списков фильмов по movie_id с сайта
        top_directors(n):Возвращает словарь с топ-n режиссерами и количеством их фильмов.
        most_expensive(n): Возвращает словарь с топ-n самых дорогих фильмов и их бюджетами.
        most_profitable(n): Возвращает словарь с топ-n самых прибыльных фильмов и их прибылью.
        longest(n): Возвращает словарь с топ-n самых длинных фильмов и их продолжительностью в мин.
        top_cost_per_minute(n): Возвращает словарь с топ-n фильмов по стоимости за минуту.
    """

    def __init__(self, path_to_the_file: str):
        """
        Инициализирует класс Links с путем к файлу links.csv.

        Атрибуты:
            path_to_the_file: str, путь к CSV файлу.
        """
        self.path = path_to_the_file
        self.links_data = self.__load_links()

    def __load_links(self) -> list:
        """
        Загружает данные из файла links.csv.

        Возвращает:
            список, представляющих строки в файле CSV.
        """
        try:
            links = []
            with open(self.path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    links.append(row)
            return links

        except Exception as e:
            print(f"Error reading file: {e}")

    def __get_soup(self, imdb_id: str) -> BeautifulSoup:
        """
        Парсит сайт и переводит html в читаемый вид через BS4

        Атрибуты:
            imdb_id: str, идентификатор IMDb для movieId.

        Возвращает:
            soup: объект BeautifulSoup.
        """
        if not imdb_id or not isinstance(imdb_id, str):
            print("Invalid IMDb ID passed to __get_soup")
            return None

        url = "https://www.imdb.com/"
        imdb_id = imdb_id.strip("/")

        if imdb_id.isdigit():
            imdb_id = f"tt{imdb_id}"

        if imdb_id.startswith("tt"):
            url = f"{url}title/{imdb_id}/"
        elif imdb_id.startswith("nm"):
            url = f"{url}name/{imdb_id}/"
        elif imdb_id.startswith("name/nm"):
            url = f"{url}{imdb_id}/"
        elif imdb_id.startswith("title/tt"):
            url = f"{url}{imdb_id}/"
        else:
            url = f"{url}{imdb_id}/"

        print(f"url = {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0)\
                Gecko/20100101 Firefox/133.0"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        except requests.exceptions.RequestException as ex:
            print(f"Error fetching URL: {url}")
            return None

    def get_imdb(self, movie_ids: list, list_of_fields: list) -> list[list]:
        """
        Получаем список списков для фильмов по movie_ids(movieId) с сайта фильмов
        Например, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].

        Атрибуты:
            movie_ids: list, идентификаторы фильмов (movieId).
            list_of_fields: list, поля для извлечения с IMDb страниц.

        Возвращает:
            Список списков фильмов отсортированных по убыванию.
        """
        imdb_info = []
        for movie_id in movie_ids:
            imdb_id = self.__get_imdb_id(movie_id)
            if imdb_id:
                movie_data = [movie_id]
                soup = self.__get_soup(imdb_id)
                if soup is None:
                    continue
                for field in list_of_fields:
                    value = self.__extract_field(soup, field)
                    movie_data.append(value)

                imdb_info.append(movie_data)

        imdb_info.sort(key=lambda x: x[0], reverse=True)
        return imdb_info

    def __get_imdb_id(self, movie_id: int) -> str:
        """
        Получает идентификатор IMDb для указанного movieId.

        Атрибуты:
            movie_id: int, идентификатор фильма.

        Возвращает:
            str, идентификатор IMDb или None.
        """
        for row in self.links_data:
            try:
                if int(row["movieId"]) == movie_id:
                    return row["imdbId"]
            except (ValueError, KeyError):
                continue
        return None

    def __extract_field(self, soup: BeautifulSoup, field: str) -> str:
        """
        Извлекает указанное поле с IMDb страницы.

        Атрибуты:
            soup: объект BeautifulSoup.
            field: str, поле для извлечения.

        Возвращает:
            str, извлеченное значение или None.
        """
        field_mapping = {}
        if field == "Director":
            director = self.__get_director(soup)
            field_mapping["Director"] = director
        elif field == "Budget":
            budget = self.__get_budget(soup)
            field_mapping["Budget"] = budget
        elif field == "Cumulative Worldwide Gross":
            gross = self.__get_gross(soup)
            field_mapping["Cumulative Worldwide Gross"] = gross
        elif field == "Runtime":
            runtime = self.__get_runtime(soup)
            field_mapping["Runtime"] = runtime

        if field in field_mapping:
            return field_mapping[field]

        return None

    def __get_director(self, soup: BeautifulSoup) -> str:
        """
        Достаем имя режисера

        Атрибуты:
            soup: объект BeautifulSoup.

        Возвращает:
            str, имя режисера выпеустившего фильм
        """
        try:
            credit_block = soup.find("li", {"data-testid": "title-pc-principal-credit"})
            if credit_block:
                director_tag = credit_block.find("a")
                if director_tag:
                    return director_tag.text.strip()
        except AttributeError:
            return None

    def __get_budget(self, soup: BeautifulSoup) -> str:
        """
        Достаем бюджет фильма

        Атрибуты:
            soup: объект BeautifulSoup.

        Возвращает:
            str, бюджет фильма
        """
        try:
            budget = (
                soup.find("li", {"data-testid": "title-boxoffice-budget"})
                .find("span", {"class": "ipc-metadata-list-item__list-content-item"})
                .text.strip()
            )
            return budget
        except AttributeError:
            return None

    def __get_gross(self, soup: BeautifulSoup) -> str:
        """
        Дотсаем совокупный мировой сбор на фильм

        Атрибуты:
            soup: объект BeautifulSoup.

        Возвращает:
            str, совокупный мировой сбор на фильм
        """
        try:
            gross = (
                soup.find(
                    "li", {"data-testid": "title-boxoffice-cumulativeworldwidegross"}
                )
                .find("span", {"class": "ipc-metadata-list-item__list-content-item"})
                .text.strip()
            )
            return gross
        except AttributeError:
            return None

    def __get_runtime(self, soup: BeautifulSoup) -> str:
        """
        Достаем длительность фильма

        Атрибуты:
            soup: объект BeautifulSoup.

        Возвращает:
            str, длительность фильма, формата h:m
        """
        try:
            runtime = soup.find("span", {"class": "sc-d7fcdef3-4 kjcuO"}).text.strip()
            return runtime
        except AttributeError:
            return None

    def top_directors(self, n: int) -> dict:
        """
        Возвращает словарь с топ-n режиссерами и количеством их фильмов.

        Аргументы:
            n: int, количество лучших режиссеров для возврата.

        Возвращает:
            dict, {имя_режиссера: количество_фильмов}, sort по кол-ву фильмов по убыванию.
        """
        directors_count = {}
        processed_urls = set()

        for row in self.links_data:
            imdb_id = row.get("imdbId")
            if not imdb_id:
                continue

            soup = self.__get_soup(imdb_id)
            if soup is None:
                continue

            credit_block = soup.find("li", {"data-testid": "title-pc-principal-credit"})
            if not credit_block:
                continue

            director_tag = credit_block.find("a")
            if not director_tag:
                continue

            director_name = director_tag.text.strip()
            director_href = director_tag.get("href")

            if not director_href:
                continue

            parsed_href = urlparse(director_href)._replace(query="").geturl()
            director_href = parsed_href.strip("/")

            if director_href in processed_urls:
                continue
            processed_urls.add(director_href)

            director_soup = self.__get_soup(director_href)

            if director_soup is None:
                continue

            try:
                count_button = director_soup.find(
                    "button", {"id": "name-filmography-filter-director"}
                )
                count_span = (
                    count_button.find("span", class_="ipc-chip__count")
                    if count_button
                    else None
                )
                if count_span:
                    film_count = int(count_span.text.strip())
                    directors_count[director_name] = film_count
            except Exception:
                continue

        sorted_directors = dict(
            sorted(directors_count.items(), key=lambda x: x[1], reverse=True)[:n]
        )
        return sorted_directors

    def most_expensive(self, n: int) -> dict:
        """
        Возвращает словарь с топ-n самых дорогих фильмов и их бюджетами.

        Аргументы:
            n: int, количество лучших фильмов для возврата.

        Возвращает:
            dict, {название_фильма: бюджет}, отсортированный по бюджету по убыванию.
        """
        budgets = []

        for row in self.links_data:
            imdb_id = row["imdbId"]
            soup = self.__get_soup(imdb_id)
            if soup is None:
                continue

            budget_str = self.__extract_field(soup, "Budget")
            if not budget_str:
                continue

            digits = re.findall(r"\d+", budget_str.replace(",", ""))
            if not digits:
                continue

            budget_value = int("".join(digits))
            title = soup.find("h1").text.strip()
            budgets.append((title, budget_value, budget_str))

        sorted_budgets = sorted(budgets, key=lambda x: x[1], reverse=True)[:n]

        return {title: budget_str for title, _, budget_str in sorted_budgets}

    def most_profitable(self, n: int) -> dict:
        """
        Возвращает словарь с топ-n самых прибыльных фильмов и их прибылью.

        Аргументы:
            n: int, количество лучших фильмов для возврата.

        Возвращает:
            dict, {название_фильма: прибыль}, отсортированный по прибыли по убыванию.
        """
        profits = {}
        for row in self.links_data:
            imdb_id = row["imdbId"]
            soup = self.__get_soup(imdb_id)
            budget = self.__extract_field(soup, "Budget")
            gross = self.__extract_field(soup, "Cumulative Worldwide Gross")
            if budget and gross:
                title = soup.find("h1").text.strip()
                profit = int("".join(re.findall(r"\d+", gross))) - int(
                    "".join(re.findall(r"\d+", budget))
                )
                profits[title] = profit

        sorted_profits = dict(
            sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n]
        )
        return sorted_profits

    def longest(self, n: int) -> dict:
        """
        Возвращает словарь с топ-n самых длинных фильмов и их продолжительностью в минутах.

        Аргументы:
            n: int, количество лучших фильмов для возврата.

        Возвращает:
            dict, {название_фильма: продолжительность}, sort по продолжительности по убыванию.
        """
        runtimes = {}
        for row in self.links_data:
            imdb_id = row["imdbId"]
            soup = self.__get_soup(imdb_id)
            runtime = self.__extract_field(soup, "Runtime")
            if runtime:
                title = soup.find("h1").text.strip()
                hour = int(runtime.split(":")[0])
                minute = int(runtime.split(":")[1])
                runtimes[title] = hour * 60 + minute

        sorted_runtimes = dict(
            sorted(runtimes.items(), key=lambda x: x[1], reverse=True)[:n]
        )
        return sorted_runtimes

    def top_cost_per_minute(self, n: int) -> dict:
        """
        Возвращает словарь с топ-n фильмов по стоимости за минуту.

        Аргументы:
            n: int, количество лучших фильмов для возврата.

        Возвращает:
            dict, {название_фильма: стоимость_за_минуту}, sort по стоимости за минуту по убыванию.
        """
        cost_per_minute = {}
        for row in self.links_data:
            imdb_id = row["imdbId"]
            soup = self.__get_soup(imdb_id)
            budget = self.__extract_field(soup, "Budget")
            runtime = self.__extract_field(soup, "Runtime")
            if budget and runtime:
                try:
                    title = soup.find("h1").text.strip()
                    hour = int(runtime.split(":")[0])
                    minute = int(runtime.split(":")[1])
                    cost = round(
                        int("".join(re.findall(r"\d+", budget)))
                        / int(hour * 60 + minute),
                        2,
                    )
                    cost_per_minute[title] = cost
                except Exception:
                    continue

        sorted_costs = dict(
            sorted(cost_per_minute.items(), key=lambda x: x[1], reverse=True)[:n]
        )
        return sorted_costs
