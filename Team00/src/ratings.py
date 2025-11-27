"""
Модуль для анализа рейтингов фильмов из датасета MovieLens.

Содержит класс Ratings, включающий вложенные классы Movies и Users
для анализа оценок по фильмам и пользователям соответственно.

Предоставляет методы для анализа распределений по годам, оценкам,
поиска самых популярных, противоречивых фильмов и пользователей.
"""

import pandas as pd
from datetime import datetime


class Ratings:
    """
    Класс для анализа данных из файла ratings.csv.

    Атрибуты:
        path: путь к файлу ratings.csv
        data: DataFrame с данными из файла

    Вложенные классы:
        Movies: Методы анализа по фильмам
        Users: Методы анализа по пользователям
    """

    def __init__(self, path_to_the_file: str):
        """
        Инициализирует класс Ratings с путем к файлу ratings.csv.

        Атрибуты:
            path_to_the_file: str, путь к CSV файлу.
        """
        self.path = path_to_the_file
        self.data = pd.read_csv(path_to_the_file)

    class Movies:
        """
        Класс для анализа рейтингов по фильмам.

        Методы:
            dist_by_year(): Распределение количества оценок по годам.
            dist_by_rating(): Распределение количества оценок по рейтингу.
            top_by_num_of_ratings(n): Топ-n фильмов по числу оценок.
            top_by_ratings(n, metric): Топ-n фильмов по среднему или медианному рейтингу.
            top_controversial(n): Топ-n самых противоречивых фильмов (по дисперсии).
        """

        def __init__(self, ratings_df: pd.DataFrame):
            """
            Инициализирует вложенный класс Movies с переданным DataFrame.

            Аргументы:
                ratings_df: DataFrame с колонками userId, movieId, rating, timestamp.
            """
            self.data = ratings_df

        def dist_by_year(self) -> dict:
            """
            Возвращает распределение оценок по годам на основе timestamp.

            Возвращает:
                dict: {год: количество оценок}, отсортировано по возрастанию года.
            """
            self.data["year"] = pd.to_datetime(self.data["timestamp"], unit="s").dt.year
            return dict(self.data["year"].value_counts().sort_index())

        def dist_by_rating(self) -> dict:
            """
            Возвращает распределение оценок по значениям рейтингов.

            Возвращает:
                dict: {рейтинг: количество}, отсортировано по возрастанию рейтинга.
            """
            return dict(self.data["rating"].value_counts().sort_index())

        def top_by_num_of_ratings(self, n: int) -> dict:
            """
            Возвращает top-n фильмов по количеству оценок.

            Аргументы:
                n: int, количество фильмов для возврата.

            Возвращает:
                dict: {movieId: число оценок}, сортировка по убыванию.
            """
            result = self.data["movieId"].value_counts().head(n)
            return dict(result)

        def top_by_ratings(self, n: int, metric: str = "average") -> dict:
            """
            Возвращает top-n фильмов по среднему или медианному рейтингу.

            Аргументы:
                n: int, количество фильмов для возврата.
                metric: str, 'average' или 'median'.

            Возвращает:
                dict: {movieId: значение метрики}, сортировка по убыванию.
            """
            grouped = self.data.groupby("movieId")["rating"]
            if metric == "average":
                agg = grouped.mean()
            elif metric == "median":
                agg = grouped.median()
            else:
                raise ValueError("Invalid metric. Use 'average' or 'median'.")
            agg = agg.round(2).sort_values(ascending=False).head(n)
            return dict(agg)

        def top_controversial(self, n: int) -> dict:
            """
            Возвращает top-n фильмов по дисперсии оценок.

            Аргументы:
                n: int, количество фильмов для возврата.

            Возвращает:
                dict: {movieId: дисперсия}, отсортировано по убыванию.
            """
            var = self.data.groupby("movieId")["rating"].var().round(2)
            var = var.dropna().sort_values(ascending=False).head(n)
            return dict(var)

    class Users:
        """
        Класс для анализа рейтингов по пользователям. Наследует методы от Movies.

        Методы:
            dist_by_num_of_ratings(): Распределение пользователей по числу оценок.
            dist_by_rating(metric): Распределение пользователей по среднему или медианному рейтингу.
            top_controversial(n): Топ-n пользователей по дисперсии оценок.
        """

        def __init__(self, ratings_df: pd.DataFrame):
            """
            Инициализирует вложенный класс Users с переданным DataFrame.

            Аргументы:
                ratings_df: DataFrame с колонками userId, movieId, rating, timestamp.
            """
            self.data = ratings_df

        def dist_by_num_of_ratings(self) -> dict:
            """
            Возвращает распределение пользователей по количеству оценок.

            Возвращает:
                dict: {userId: количество оценок}, отсортировано по userId.
            """
            return dict(self.data["userId"].value_counts().sort_index())

        def dist_by_rating(self, metric: str = "average") -> dict:
            """
            Возвращает распределение пользователей по средней или медианной оценке.

            Аргументы:
                metric: str, 'average' или 'median'.

            Возвращает:
                dict: {userId: значение метрики}, отсортировано по userId.
            """
            grouped = self.data.groupby("userId")["rating"]
            if metric == "average":
                agg = grouped.mean()
            elif metric == "median":
                agg = grouped.median()
            else:
                raise ValueError("Invalid metric. Use 'average' or 'median'.")
            return dict(agg.round(2).sort_index())

        def top_controversial(self, n: int) -> dict:
            """
            Возвращает top-n пользователей по дисперсии оценок.

            Аргументы:
                n: int, количество пользователей для возврата.

            Возвращает:
                dict: {userId: дисперсия}, отсортировано по убыванию дисперсии.
            """
            var = self.data.groupby("userId")["rating"].var().round(2)
            var = var.dropna().sort_values(ascending=False).head(n)
            return dict(var)

        def most_active_users(self, n: int) -> dict:
            """
            Возвращает top-n пользователей по кол-ву оценок

            Аргументы:
                n: int, количество пользователей для возврата.

            Возвращает:
                dict: {userId: кол-во оценок}
            """
            count = self.data["userId"].value_counts().head(n)
            return dict(count)
