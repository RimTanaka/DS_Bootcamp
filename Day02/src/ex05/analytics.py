"""
Файл для обработки данных из CSV файла.
Класс Research:
    - Обрабатывает файл, проверяя корректность данных.
Класс Calculations:
    - Выполняет расчеты на основе обработанных данных.
"""
from random import randint


class Research:
    """
    Класс, который обрабатывает чтение и проверку данных из файла.

    Атрибуты:
        path (str): Путь к файлу для обработки.
        has_header (bool): определяет будем ли искать заголовок у файла
    """

    def __init__(self, path: str, has_header: bool = True):
        self.path = path
        self.has_header = has_header

    def __read_file(self) -> list:
        """
        Считывает файл и возвращает его содержимое в виде списка строк.

        Возвращает:
            list: Список строк, считанных из файла.

        Исключения:
            FileNotFoundError: Если файл не найден.
        """
        try:
            with open(self.path, "r", encoding='utf-8') as file:
                return file.readlines()
        except FileNotFoundError as exc:
            raise FileNotFoundError("File not found. Check the path.") from exc

    def __check_lines(self, lines: list) -> list:
        """
        Обрабатывает строки из файла: проверяет заголовок и структуру данных.

        Возвращает:
            list: Список строк, если прошли проверку.

        Исключения:
            ValueError: Если структура данных в файле неверна.
        """
        if self.has_header:
            header = lines[0].strip()
            if header != "head,tail":
                raise ValueError("Invalid file header.")
            lines = lines[1:]

        result = []
        for line in lines:
            tmp_line = line.strip().split(',')
            if (
                len(tmp_line) != 2
                or not (int(tmp_line[0]) in [0, 1]
                        and int(tmp_line[1]) in [0, 1])
                or tmp_line[0] == tmp_line[1]
            ):
                raise ValueError(
                    f"Invalid Structure value '{line.strip()}' in file."
                )
            result.append([int(tmp_line[0]), int(tmp_line[1])])
        return result

    def file_reader(self) -> list:
        """
        Считывает файл, проверяет на ошибки и возвращает список строк.

        Возвращает:
            str: Строку, прошедшую проверку.

        Исключения:
            ValueError: Если структура данных в файле неверна.
            FileNotFoundError: Если файл не найден.
        """
        lines = self.__read_file()
        res = self.__check_lines(lines)
        return res

    class Calculations:
        """
        Вложенный класс для выполнения расчетов на основе данных.
        """

        def __init__(self, data: list):
            self.data = data

        def counts(self) -> tuple:
            """
            Подсчитывает количество орлов и решек в данных.

            Аргументы:
                data (list): Список списков, содержащий данные.

            Возвращает:
                tuple: Количество орлов и решек (heads, tails).
            """
            heads_count = sum(row[0] for row in self.data)
            tails_count = sum(row[1] for row in self.data)
            return heads_count, tails_count

        def fractions(self, heads_count: int, tails_count: int) -> tuple:
            """
            Вычисляет доли орлов и решек в процентах.

            Аргументы:
                heads_count (int): Количество орлов.
                tails_count (int): Количество решек.

            Возвращает:
                tuple: Доли орлов и решек в % (head_fraction, tail_fraction).
            """
            total = heads_count + tails_count
            if total == 0:
                return 0, 0
            return (heads_count / total) * 100, (tails_count / total) * 100


class Analytics(Research.Calculations):
    """
    Класс для расширенного анализа, наследуется от Calculations.
    """

    def predict_random(self, step: int) -> list:
        """
        Генерирует список случайных прогнозов.

        Аргументы:
            step (int): Количество прогнозов, которые нужно сгенерировать.

        Возвращает:
            list: Список списков вида [[1, 0], [0, 1]], где каждая пара
            представляет одну случайную симуляцию орла и решки.

        Пример:
            Для steps=3 результат может быть таким: [[1, 0], [1, 0], [0, 1]].
        """
        res = []
        for _ in range(step):
            tmp = randint(0, 1)
            res.append([tmp, 1 if tmp == 0 else 0])
        return res

    def predict_last(self) -> list:
        """
        Возвращает последний элемент из данных.

        Возвращает:
            list: Последняя строка данных в формате [head, tail],
            если данные существуют. Если данных нет, возвращает пустой список.

        Пример:
            Если self.data = [[0, 1], [0, 1], [1, 0]], метод вернет [1, 0].
        """
        return self.data[-1] if self.data else []

    def save_file(self, data: str, file_name: str, extension: str) -> None:
        """
        Сохраняет результат в файл с указанным расширением.

        Аргументы:
            data: str: данные которе нужно сохранить
            file_name: str: название файла
            extension: str: расширение файла

        Возвращает:
            None: Метод ничего не возвращает
        """
        with open(f"{file_name}.{extension}", "w", encoding="utf-8") as file:
            file.write(data)
