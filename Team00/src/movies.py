"""
Модуль для анализа информации о фильмах из файла movies.csv.

Содержит класс Movies, предоставляющий методы для анализа распределения
фильмов по годам, жанрам и количеству жанров.
"""

from collections import Counter
from collections import OrderedDict
import pandas as pd
import re


class Movies:
    """
    Класс для анализа данных из файла movies.csv.

    Атрибуты:
        path_to_the_file: str — путь к файлу movies.csv.

    Методы:
        dist_by_release(): Возвращает словарь с количеством фильмов по годам.
        dist_by_genres(): Возвращает словарь с количеством фильмов по жанрам.
        most_genres(n): Возвращает словарь с топ-n фильмов по количеству жанров.
    """

    def __init__(self, path_to_the_file: str):
        """
        Инициализирует класс Movies с путем к файлу movies.csv.

        Аргументы:
            path_to_the_file: str, путь к CSV файлу.
        """
        self.path = path_to_the_file
        self.data = pd.read_csv(path_to_the_file)

    def dist_by_release(self) -> OrderedDict:
        """
        Возвращает количество фильмов, выпущенных в каждый год.

        Извлекает год выпуска из названия фильма (например, "Toy Story (1995)")
        и считает количество фильмов для каждого года.

        Возвращает:
            OrderedDict — словарь вида {год: количество}, отсортированный по убыванию.
        """
        years = self.data["title"].apply(lambda title: re.search(r"\((\d{4})\)", title))
        year_list = [match.group(1) for match in years if match]
        counter = Counter(year_list)
        sorted_years = OrderedDict(
            sorted(counter.items(), key=lambda x: x[1], reverse=True)
        )
        return sorted_years

    def dist_by_genres(self) -> dict:
        """
        Возвращает количество фильмов по каждому жанру.

        Разбивает строку жанров (через '|') и подсчитывает общее количество
        появлений каждого жанра во всех фильмах.

        Возвращает:
            dict — словарь вида {жанр: количество}, отсортированный по убыванию.
        """
        all_genres = self.data["genres"].str.split("|").sum()
        counter = Counter(all_genres)
        sorted_genres = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
        return sorted_genres

    def most_genres(self, n: int) -> dict:
        """
        Возвращает топ-n фильмов с наибольшим количеством жанров.

        Для каждого фильма считает количество жанров и возвращает n фильмов
        с наибольшим значением.

        Аргументы:
            n: int — количество фильмов в результате.

        Возвращает:
            dict — словарь вида {название_фильма: количество_жанров}, отсортированный по убыванию.
        """
        self.data["genre_count"] = self.data["genres"].apply(
            lambda g: len(g.split("|")) if isinstance(g, str) else 0
        )
        top_n = (
            self.data[["title", "genre_count"]]
            .sort_values(by="genre_count", ascending=False)
            .head(n)
        )
        return dict(zip(top_n["title"], top_n["genre_count"]))
