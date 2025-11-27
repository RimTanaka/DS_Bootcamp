#!/usr/bin/env python3
"""
Модуль для вывода пути к виртуальному окружению

Возвращает:
    - Если вкл env 'Your current virtual env is {Path}'
    - Если выкл env 'Error env is off'
"""
import os


if __name__ == "__main__":
    try:
        print(f"Your current virtual env is {os.environ['VIRTUAL_ENV']}")
    except KeyError as e:
        print(f"Error {e} is off")
