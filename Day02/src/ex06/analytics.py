"""
Файл для обработки данных из CSV файла.

Класс Research:
    - Обрабатывает файл, проверяя корректность данных.

Класс Calculations:
    - Выполняет расчеты на основе обработанных данных.
"""

from random import randint
import requests
import my_token
from config import logger


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
        logger.info(
            "Инициализация класса Research, path: %s и has_header: %s",
            self.path,
            str(self.has_header),
        )

    def __read_file(self) -> list:
        """
        Считывает файл и возвращает его содержимое в виде списка строк.

        Возвращает:
            list: Список строк, считанных из файла.

        Исключения:
            FileNotFoundError: Если файл не найден.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                logger.info("File %s успешно открыт.", self.path)
                return file.readlines()
        except FileNotFoundError as exc:
            logger.error("File %s не найден. {exc}", self.path)
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
                logger.warning("Неверный header: %s", header)
                raise ValueError("Invalid file header.")
            lines = lines[1:]

        result = []
        for line in lines:
            tmp_line = line.strip().split(",")
            if (
                len(tmp_line) != 2
                or not (int(tmp_line[0]) in [0, 1]
                        and int(tmp_line[1]) in [0, 1])
                or tmp_line[0] == tmp_line[1]
            ):
                logger.error("Неверная структура данных: %d", line.strip())
                raise ValueError(f"Invalid Structure value "
                                 f"'{line.strip()}' in file.")
            result.append([int(tmp_line[0]), int(tmp_line[1])])
        logger.info("Успешно обработанно %d строк.", len(result))
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
        try:
            lines = self.__read_file()
            res = self.__check_lines(lines)
            logger.info("Файл прочитан и проверен успешно.")
            return res
        except (FileNotFoundError, ValueError) as ex:
            logger.error("Ошибка чтения файла: %s", ex)
            raise

    def send_tg_message(self, success: bool) -> None:
        """
        Отправляет сообщение в Telegram канал через Webhook.

        Аргументы:
            success (bool): Если True, успешное создание отчета,
                             если False — сообщение об ошибке.
        """
        url = my_token.URL
        chat_id = my_token.CHAT_ID
        message = (
            "The report has been successfully created."
            if success
            else "The report hasn’t been created due to an error."
        )

        params = {"chat_id": chat_id, "text": message}

        try:
            response = requests.post(url, data=params, timeout=20)
            if response.status_code == 200:
                logger.info("Telegram сообщение отправленно: %s", message)
            else:
                logger.error(
                    "Ошибка отправки сообщения в Telegram. Status code: %d",
                    response.status_code,
                )
        except requests.exceptions.RequestException as ex:
            logger.error("Error отправки Telegram сообщения: %s", ex)

    class Calculations:
        """
        Вложенный класс для выполнения расчетов на основе данных.
        """

        def __init__(self, data: list):
            self.data = data
            logger.info(
                "Инициализация класса Calculations, длинна данных: %d.",
                len(data)
            )

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
            logger.info(
                "Calculated counts: heads=%d, tails=%d",
                heads_count,
                tails_count
            )
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
                logger.warning("Total = 0.")
                return 0, 0
            logger.info(
                "Calculated fractions: heads=%.2f%%, tails=%.2f%%",
                (heads_count / total) * 100,
                (tails_count / total) * 100,
            )
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
        logger.info("Генерируем %d random.", step)
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
        logger.info("Последний элемент: %s",
                    {self.data[-1] if self.data else []})
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
            logger.info("Файл %s.%s сохранен", file_name, extension)
