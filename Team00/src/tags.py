"""
Модуль для анализа тегов из файла tags.csv.

Содержит класс Tags, который позволяет определить самые длинные,
самые популярные и самые насыщенные словами теги, а также производить
поиск по ключевому слову.
"""

import pandas as pd


class Tags:
    """
    Класс для анализа данных из файла tags.csv.

    Атрибуты:
        path: Путь к файлу tags.csv.
        data: DataFrame с загруженными данными.

    Методы:
        most_words(n): Возвращает top-n тегов с наибольшим количеством слов.
        longest(n): Возвращает top-n самых длинных тегов по количеству символов.
        most_words_and_longest(n): Возвращает пересечение самых длинных и самых словесных тегов.
        most_popular(n): Возвращает top-n самых популярных тегов по количеству упоминаний.
        tags_with(word): Возвращает уникальные теги, содержащие заданное слово.
    """

    def __init__(self, path_to_the_file: str):
        """
        Инициализирует класс Tags с путем к файлу tags.csv.

        Атрибуты:
            path_to_the_file: str, путь к CSV файлу.
        """
        self.path = path_to_the_file
        self.data = pd.read_csv(path_to_the_file)

    def most_words(self, n: int) -> dict:
        """
        Возвращает top-n тегов с наибольшим количеством слов внутри.

        Возвращает:
            dict: {тег: количество_слов}, отсортировано по убыванию.
        """
        tags = self.data["tag"].drop_duplicates()
        tag_word_counts = tags.apply(lambda x: len(str(x).split()))
        top = tag_word_counts.sort_values(ascending=False).head(n)
        return dict(zip(tags[top.index], top))

    def longest(self, n: int) -> list:
        """
        Возвращает top-n самых длинных тегов по количеству символов.

        Возвращает:
            list: список тегов, отсортированных по убыванию длины.
        """
        tags = self.data["tag"].drop_duplicates()
        sorted_tags = tags.sort_values(key=lambda x: x.str.len(), ascending=False)
        return sorted_tags.head(n).tolist()

    def most_words_and_longest(self, n: int) -> list:
        """
        Возвращает пересечение top-n тегов по количеству слов и top-n по длине.

        Возвращает:
            list: список уникальных тегов в пересечении, отсортированный.
        """
        most_words_set = set(self.most_words(n).keys())
        longest_set = set(self.longest(n))
        return sorted(most_words_set & longest_set)

    def most_popular(self, n: int) -> dict:
        """
        Возвращает top-n самых популярных тегов по количеству упоминаний.

        Возвращает:
            dict: {тег: количество}, отсортировано по убыванию количества.
        """
        tag_counts = self.data["tag"].value_counts()
        return tag_counts.head(n).to_dict()

    def tags_with(self, word: str) -> list:
        """
        Возвращает все уникальные теги, содержащие заданное слово (без учета регистра).

        Возвращает:
            list: отсортированный список тегов, содержащих слово.
        """
        word_lower = word.lower()
        tags = self.data["tag"].drop_duplicates()
        filtered_tags = tags[tags.str.lower().str.contains(word_lower, na=False)]
        return sorted(filtered_tags.tolist())
