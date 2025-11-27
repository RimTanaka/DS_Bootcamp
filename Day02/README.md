# OOP Python Rush — Техническое задание

---

## Exercise 00 — Простой класс

**Папка:** `ex00/`  
**Файл:** `first_class.py`  
**Импорты:** запрещены

**Задача:**

- создать класс `Must_read`;
- он должен **прочитать файл `data.csv`** и **распечатать его содержимое**;
- имя файла можно захардкодить;
- `print()` должен находиться *внутри класса* (пока без методов и конструктора).

Вывод должен полностью совпадать с содержимым `data.csv`.

---

## Exercise 01 — Метод

**Папка:** `ex01/`  
**Файл:** `first_method.py`  
**Импорты:** запрещены

**Задача:**

- создать класс `Research`;
- переместить логику чтения файла в метод `file_reader()`;
- вместо `print()` метод должен возвращать данные (`return`);
- при запуске скрипт должен выводить содержимое `data.csv`.

---

## Exercise 02 — Конструктор

**Папка:** `ex02/`  
**Файл:** `first_constructor.py`  
**Разрешённые импорты:** `sys`, `os`

**Задача:**

- изменить класс `Research`:
  - добавить конструктор `__init__(path_to_file)`;
  - путь к файлу передаётся как аргумент командной строки;
- метод `file_reader()` должен:
  - читать файл, путь берётся из конструктора;
  - возвращать содержимое файла;
  - проверять структуру файла:
    - заголовок из двух значений,
    - строки вида `0,1` или `1,0`;
  - при ошибке — выбрасывать исключение.

Пример запуска:

```
python3 first_constructor.py data.csv
```


---

## Exercise 03 — Вложенный класс

**Папка:** `ex03/`
**Файл:** `first_nest.py`
**Разрешённые импорты:** `sys`, `os`

**Задача:**

Модифицировать класс `Research`:

### 1. Метод `file_reader(has_header=True)`:

- возвращает **список списков** вида: `[[0,1], [1,0], ...]`

- если `has_header=True`, пропускать заголовок.

### 2. Создать вложенный класс `Calculations`:

Методы:

- `counts(data)`
→ возвращает количество `[0,1]` и количество `[1,0]`.

- `fractions(heads, tails)`
→ возвращает проценты долей (например, `30.0` и `70.0`).

### 3. Скрипт выводит:

1. данные из `file_reader()`,
2. результаты `counts()`,
3. результаты `fractions()`.

---

## Exercise 04 — Наследование

**Папка:** `ex04/`
**Файл:** `first_child.py`
**Разрешённые импорты:** `sys`, `from random import randint`

### Изменения:

- в классе `Calculations`:
- переместить `data` в конструктор (`__init__`);
- создать класс `Analytics`, наследуемый от `Calculations`.

### Новые методы в `Analytics`:

- `predict_random(n)`
→ возвращает список из `n` псевдослучайных наблюдений типа `[1,0]` или `[0,1]`.

- `predict_last()`
→ возвращает **последний элемент** данных.

### Скрипт должен вывести:

1. данные из `file_reader()`
2. counts
3. fractions
4. результат `predict_random(3)`
5. результат `predict_last()`

---

## Exercise 05 — Конфиг и главный модуль

**Папка:** `ex05/`
**Файлы:** `config.py`, `analytics.py`, `make_report.py`
**Разрешённые импорты:** `os`, `randint`

### Требуется:

1. Создать `config.py`, в котором хранить:
 - параметры программы (например `num_of_steps`);
 - текст шаблона отчёта.

2. Переделать старый скрипт:
 - убрать логику из блока `if __name__ == '__main__'`;
 - сохранить класс в файл `analytics.py`.

3. Добавить в `Analytics` метод: `save_file(data, filename, extension)`


4. Создать скрипт `make_report.py`, который:
   - импортирует `config` и `analytics`;
   - формирует текст отчёта;
   - сохраняет его в файл.

**Пример отчёта:**

```
Report
We have made 12 observations from tossing a coin: 5 of them were tails and 7 of
them were heads. The probabilities are 41.67% and 58.33%, respectively. Our
forecast is that in the next 3 observations we will have: 1 tail and 2 heads.
```


---

## Exercise 06 — Логирование + Telegram

**Папка:** `ex06/`
**Файлы:** `config.py`, `analytics.py`, `make_report.py`
**Разрешённые импорты:**
`os`, `randint`, `logging`, `requests` (или `urllib`), `json`

### Требуется:

### 1. Логирование

- каждый метод всех классов должен писать лог;
- файл логов: **analytics.log**;
- формат: `2020-05-01 22:16:16,877 Calculating the counts of heads and tails`


### 2. Telegram-уведомление

В классе `Research` добавить метод:

- отправляет сообщение в Telegram через webhook:
  - «The report has been successfully created»
  - или
    «The report hasn’t been created due to an error»

### 3. Примечания:

- `config.py` может содержать переменные в глобальной области.
- В `config.py` и `analytics.py` **не нужен** блок
  `if __name__ == '__main__'`.

---



