"""
Программа определяет класс `Research` для чтения и проверки данных из файла.
Файл должен содержать разделенные запятыми значения.
Header является `head,tail`.
Первый столбец и второй столбец являются двоичными (0 или 1).
Значение в строке не повторяется.
"""
import sys


class Research:
    """
    Класс, который обрабатывает чтение и проверку данных из файла.

    Атрибуты:
    path (str): Путь к файлу для обработки.
    """

    def __init__(self, path: str):
        self.path = path

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

    def __process_lines(self, lines: list) -> list:
        """
        Обрабатывает строки из файла: проверяет заголовок и структуру данных.

        Возвращает:
            list: Список строк, прошедших проверку.

        Исключения:
            ValueError: Если структура данных в файле неверна.
        """
        header = lines[0].strip()
        if header != "head,tail":
            raise ValueError("Invalid Header '{header}' in file.")

        lines = lines[1:]
        result = [header]
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

            result.append(line.strip())
        return result

    def file_reader(self) -> str:
        """
        Считывает файл, проверяет на ошибки и возвращает список строк.

        Возвращает:
            str: Строку, прошедшую проверку.

        Исключения:
            ValueError: Если структура данных в файле неверна.
            FileNotFoundError: Если файл не найден.
        """
        lines = self.__read_file()
        check_lines = self.__process_lines(lines)
        return '\n'.join(check_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>")
        sys.exit(1)

    arg = sys.argv[1]
    research = Research(arg)
    DATA = research.file_reader()
    print(DATA)
