#!/usr/bin/env python3
"""
Модуль для установки N-ного кол-ва библиотек из файла lib.txt
"""
import os
import zipfile
import sys


def check_virtual_env():
    """
    Проверяет виртуальное окружение, если выключено то выбрасывает исключение.

    Возвращает: None.
    """
    if os.environ.get("VIRTUAL_ENV") is None:
        raise EnvironmentError(
            "Сначало необходимо включить виртуальное окружение."
        )


def install_libraries():
    """
    Установка библиотек из lib.txt. Если файл нет, выбрасывает исключение.

    Возвращает: None
    """
    lib = "lib.txt"
    if os.path.exists(lib):
        os.system(f"pip install -r {lib}")
    else:
        raise FileNotFoundError(f"Файл {lib} не найден.")


def save_installed_libraries():
    """
    Сохраняет установленные библиотеки в requirements.txt и выводит на экран.

    Возвращает: None.
    """
    installed_libraries = os.popen("pip freeze").read()
    with open("requirements.txt", "w", encoding="utf-8") as file:
        file.write(installed_libraries)
    print("Установленные библиотеки:")
    print(installed_libraries)


def print_progress_bar(iteration, total, length=40):
    """
    Отображает прогресс-бар.

    Атрибуты:
        - iteration: текущий шаг
        - total: общее количество шагов
        - length: длина прогресс-бара

    Возвращает: None.
    """
    percent = f"{(iteration / total) * 100:.1f}"
    filled_length = int(length * iteration // total)
    status_bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r[{status_bar}] {percent}%")
    sys.stdout.flush()


def archive_env():
    """
    Сохранение результата в ZIP архив.

    Возвращает: None.
    """
    venv_path = os.environ["VIRTUAL_ENV"]
    archive_name = os.path.basename(venv_path) + ".zip"
    #    os.system(f"zip -ruq {archive_name} {venv_path}") #> /dev/null 2>&1")
    #    print(f"Virtual env заархивирован в {archive_name}")

    file_paths = []
    for root, _, files in os.walk(venv_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    total_files = len(file_paths)

    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for i, file in enumerate(file_paths, 1):
            arcname = os.path.relpath(file, start=venv_path)
            zipf.write(file, arcname)
            print_progress_bar(i, total_files)
    print()

    print(f"Virtual env заархивирован в {archive_name}")


if __name__ == "__main__":
    check_virtual_env()
    install_libraries()
    save_installed_libraries()
    archive_env()
