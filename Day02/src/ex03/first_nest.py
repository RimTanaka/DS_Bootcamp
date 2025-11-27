"""
Программа для обработки данных из CSV файла.
Класс Research:
    - Обрабатывает файл, проверяя корректность данных.
Класс Calculations:
    - Выполняет расчеты на основе обработанных данных.
"""
import sys


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

    def get_calculations(self):
        """
        Возвращает экземпляр вложенного класса Calculations.

        Возвращает:
            Calculations: Экземпляр вложенного класса для выполнения расчетов.
        """
        return Research.Calculations()

    class Calculations:
        """
        Вложенный класс для выполнения расчетов на основе данных.
        """

        def counts(self, data: list) -> tuple:
            """
            Подсчитывает количество орлов и решек в данных.

            Аргументы:
                data (list): Список списков, содержащий данные.

            Возвращает:
                tuple: Количество орлов и решек (heads, tails).
            """
            heads_count = sum(row[0] for row in data)
            tails_count = sum(row[1] for row in data)
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


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 first_nest.py <file_path> [Header: True/False]")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        is_header = True if len(sys.argv) == 2 else sys.argv[2].lower() == "true"
        if len(sys.argv) == 3 and sys.argv[2].lower() not in ["true", "false"]:
            print("Usage: python3 first_nest.py <file_path> "
                "[Header: True/False]")
            raise ValueError("Invalid argument in has_header.")

        research = Research(file_path, is_header)
        data_file = research.file_reader()

        print(data_file)

        calc = research.get_calculations()
        heads, tails = calc.counts(data_file)
        print(heads, tails)

        head_fraction, tail_fraction = calc.fractions(heads, tails)
        print(head_fraction, tail_fraction)

    except ValueError as error:
        print(f"Error: {error}")
