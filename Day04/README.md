# Benchmarking — Техническое задание

---

## Exercise 00 — List Comprehensions

**Папка:** `ex00/`  
**Файл:** `benchmark.py`  
**Разрешённые импорты:** `timeit`

**Задача:**

- создать список `emails` из 5 уникальных адресов, повторённых 5 раз → всего 25 элементов;
- реализовать две функции:
  1. фильтрация Gmail через цикл и `append`;
  2. фильтрация Gmail через list comprehension;
- замерить время выполнения каждой функции **90 000 000 раз**;
- сравнить результаты:
  - если list comprehension быстрее или равен → вывести  
    **"it is better to use a list comprehension"**
  - иначе →  
    **"it is better to use a loop"**;
- вывести оба времени в порядке возрастания.

---

## Exercise 01 — Map

**Папка:** `ex01/`  
**Файл:** `benchmark.py`  
**Разрешённые импорты:** `timeit`

**Задача:**

- добавить третью функцию: фильтрация Gmail через `map()` и `list(map())`;
- сравнить три метода: loop / list comprehension / map;
- вывод:
  - текст вида: **"it is better to use a map"** (или другой вариант);
  - три времени, упорядоченные по возрастанию.

Пример:

```
it is better to use a map
29.32 vs 54.62 vs 55.99

```


---

## Exercise 02 — Filter

**Папка:** `ex02/`  
**Файл:** `benchmark.py`  
**Разрешённые импорты:** `timeit`, `sys`

**Задача:**

- добавить функцию фильтрации Gmail через `filter()`;
- переписать скрипт так, чтобы он принимал параметры командной строки:


```
./benchmark.py <function_name> <calls_number>
```


где `<function_name>` ∈ {`loop`, `list_comprehension`, `map`, `filter`};

- выводить только время выполнения указанного числа вызовов.

Примеры:

```
./benchmark.py loop 10000000
./benchmark.py filter 10000000
```


---

## Exercise 03 — Reduce

**Папка:** `ex03/`
**Файл:** `benchmark.py`
**Разрешённые импорты:** `timeit`, `sys`, `from functools import reduce`

**Задача:**

- реализовать две функции вычисления суммы квадратов от 1 до N:
  1. обычный цикл: `sum += i*i`;
  2. `reduce()`;
- запускается так:

```
./benchmark.py <function_name> <calls_number> <N>
```


- вывод — время выполнения `<calls_number>` вызовов.

Пример:

```
./benchmark.py loop 10000000 5
./benchmark.py reduce 10000000 5
```


---

## Exercise 04 — Counter

**Папка:** `ex04/`
**Файл:** `benchmark.py`
**Разрешённые импорты:** `timeit`, `random`, `from collections import Counter`

**Задача:**

1. сгенерировать список из 1 000 000 случайных чисел от 0 до 100;
2. написать собственную функцию подсчёта количества всех чисел;
3. написать собственную функцию получения топ-10 самых частых;
4. повторить те же операции с использованием `Counter`;
5. сравнить время выполнения.

Пример:

```
my function: 0.4501532
Counter: 0.0432341
my top: 0.1032348
Counter's top: 0.017573
```


---

## Exercise 05 — Генератор

**Папка:** `ex05/`
**Файлы:** `ordinary.py`, `generator.py`
**Допустимые импорты:**
- Linux/macOS: `sys`, `resource`
- Windows: `sys`, `os`, `psutil`

**Данные:**
скачать и распаковать MovieLens, использовать файл `ratings.csv` (~678 MB).

---

### ordinary.py

- функция читает **все строки в список**, возвращает список;
- в `main` пройтись по списку циклом (внутри `pass`);
- вывод:
  - Peak Memory Usage (GB)
  - User Mode Time + System Mode Time (sec)

---

### generator.py

- функция читает файл **построчно через `yield`**, не загружая всё в память;
- в `main` пройтись по генератору (`pass`);
- вывести те же метрики.

Пример:

```
$ ./ordinary.py ratings.csv
Peak Memory Usage = 2.114 GB
User Mode Time + System Mode Time = 5.77s

$ ./generator.py ratings.csv
Peak Memory Usage = 0.005 GB
User Mode Time + System Mode Time = 9.04s

```

---



