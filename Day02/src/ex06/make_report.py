"""
Этот модуль отвечает за создание отчета на основе данных из файла CSV\
 и сохранение его в файл.

Функции:
- make_report(path: str, has_header: bool) -> None: \
Основная функция для создания отчета и сохранения его в файл.
"""

import sys
from analytics import Research, Analytics
import config


def make_report(path: str, has_header: bool) -> None:
    """
    Генерирует отчет на основе данных из CSV файла \
и сохраняет его в текстовый файл.

    Аргументы:
        path (str): Путь к CSV файлу с данными.
        has_header (bool): Если True, файл содержит заголовок, \
который необходимо пропустить при обработке.

    Возвращает:
        None: Функция ничего не возвращает.
    """
    try:
        research = Research(path, has_header)
        data_file = research.file_reader()

        analytics = Analytics(data_file)
        heads, tails = analytics.counts()

        head_fraction, tail_fraction = analytics.fractions(heads, tails)

        random_predictions = analytics.predict_random(config.NUM_OF_STEPS)
        analytics_next_pred = Analytics(random_predictions)
        pred_head, pred_tail = analytics_next_pred.counts()

        report = config.REPORT_TEMPLATE.format(
            count_observations=len(data_file),
            tails_count=tails,
            heads_count=heads,
            tail_fraction=tail_fraction,
            head_fraction=head_fraction,
            pred_steps=config.NUM_OF_STEPS,
            pred_tails=pred_head,
            pred_heads=pred_tail,
        )

        print(report)
        analytics.save_file(report, "report", "txt")
        research.send_tg_message(success=True)

    except FileNotFoundError as ex:
        print(f"Error: {ex}")
        research.send_tg_message(success=False)
    except ValueError as ex:
        print(f"Error: {ex}")
        research.send_tg_message(success=False)


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 first_nest.py <file_path> [Header: True/False]")
        sys.exit(1)

    file_path = sys.argv[1]

    is_header = True if len(sys.argv) == 2 else sys.argv[2].lower() == "true"
    if len(sys.argv) == 3 and sys.argv[2].lower() not in ["true", "false"]:
        print("Usage: python3 first_nest.py <file_path> [Header: True/False]")
        raise ValueError("Invalid argument in Header.")

    make_report(file_path, is_header)
