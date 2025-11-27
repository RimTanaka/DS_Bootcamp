# Day — Pandas  
## Техническое задание (короткое)

---

# Exercise 00 — Load and Save

**Папка:** `ex00/`  
**Файл:** `load_and_save.ipynb`  
**Импорт:** `import pandas as pd`

### Задача
Загрузить лог-файл → очистить → сохранить в новом формате.

### Требования:

1. Прочитать файл через `pd.read_csv()`  
   - пропустить строки с индексами 2 и 3 → `skiprows`  
   - удалить последние 2 строки → `skipfooter`  
   - присвоить имена колонкам: `datetime`, `user`  
   - сделать `datetime` индексом  
   - переименовать столбец в `date_time`

2. Сохранить в новый файл `feed-views-semicolon.log`  
   - разделитель `;`

Ожидаемый результат в `df.head()` / `df.tail()` как в примере.

---

# Exercise 01 — Basic Operations

**Папка:** `ex01/`  
**Файл:** `basic_operations.ipynb`  
**Импорт:** `import pandas as pd`

### Задачи

- загрузить `feed-views.log` → создать DataFrame `views`
- привести `datetime` к типу `datetime64[ns]`
- извлечь год, месяц, день, час, минуту, секунду в новые колонки
- создать колонку `daytime`, используя `pd.cut()`  
  интервалы:
  - 0–3.59 night  
  - 4–6.59 early morning  
  - 7–10.59 morning  
  - 11–16.59 afternoon  
  - 17–19.59 early evening  
  - 20–23.59 evening
- поставить `user` как индекс
- выполнить:
  - `count()` — число записей  
  - `value_counts()` по `daytime`
  - сортировку по часам/минутам/секундам
  - min/hour, max/hour, mode()
  - max(hour) для night + кто посещал
  - min(hour) для morning + кто посещал
  - 3 самых ранних и 3 самых поздних посещения: `nsmallest()` / `nlargest()`
  - `describe()`
  - вычислить IQR по колонке `hour`

---

# Exercise 02 — Preprocessing

**Папка:** `ex02/`  
**Файл:** `preprocessing.ipynb`  
**Импорт:** `import pandas as pd`

### Задачи:

1. Загрузить CSV, поставить `ID` индексом.  
2. Посчитать количество строк через `count()`.  
3. Удалить дубликаты по колонкам `CarNumber`, `Make_n_model`, `Fines`  
   - оставить **последний**.
4. Работа с пропусками:
   - посчитать пропуски по столбцам
   - удалить колонки >500 пропусков (`thresh`)
   - заполнить `Refund` предыдущим значением (`method='ffill'`)
   - заполнить `Fines` средним
5. Разделить `Make_n_model` → колонки `Make`, `Model`  
   - с помощью `apply`
6. Удалить колонку `Make_n_model`
7. Сохранить в `auto.json` в требуемом формате списка словарей.

---

# Exercise 03 — Selects and Aggregations

**Папка:** `ex03/`  
**Файл:** `selects_n_aggs.ipynb`  
**Импорт:** `import pandas as pd`

### Задачи:

1. Загрузить `auto.json`, поставить `CarNumber` индексом.

### Selects:

- штраф > 2100  
- штраф > 2100 и `Refund == 2`  
- модели из списка: `['Focus', 'Corolla']`  
- номера из списка (5 значений)

### Агрегации:

- медиана штрафов по `Make`
- медиана штрафов по `Make` + `Model`
- количество штрафов (для доверия к медиане)
- min/max штрафов по `Make` + `Model`
- std штрафов по `Make` + `Model`

### Аналитика по номерам:

- номера по количеству штрафов (убывание)
- вывести записи для ТОП-1 номера
- номера по сумме штрафов (убывание)
- вывести записи для ТОП-1 номера
- проверить номера с разными моделями

---

# Exercise 04 — Enrichment and Transformations

**Папка:** `ex04/`  
**Файл:** `enrichment.ipynb`  
**Импорт:** `pandas`, `numpy`, `requests`

### Задача:

1. Загрузить JSON из ex02.  
   - формат float → 2 знака.
2. Создать sample из 200 строк (random_state=21):  
   - без новых уникальных комбинаций (`CarNumber`, `Make`, `Model`)
   - значения `Refund`/`Fines` брать случайно

3. Объединить sample с исходным → `concat_rows`.

4. Добавить колонку `Year`  
   - `np.random.seed(21)`  
   - случайные года 1980–2019

5. Добавить данные о владельцах:
   - загрузить `surname.json`
   - выбрать фамилии = количество уникальных `CarNumber`
   - создать DF `owners(CarNumber, SURNAME)`

6. Внести изменения:
   - добавить 5 новых строк в `fines`
   - удалить последние 20 строк из `owners`, добавить 3 новых

7. Выполнить 4 вида join:
   - inner: только общие номера  
   - outer: все  
   - left: только номера из `fines`  
   - right: только номера из `owners`

8. Сделать pivot table:  
   - строки: `CarNumber`  
   - столбцы: `Year`  
   - значения: сумма штрафов

9. Сохранить `fines.csv` и `owners.csv` без индекса.

---

# Exercise 05 — Pandas Optimizations

**Папка:** `ex05/`  
**Файл:** `optimizations.ipynb`  
**Импорты:** `pandas`, `gc`

### 1. Загрузить `fines.csv`.

### 2. Оптимизация операций:

В каждой — создать колонку: `fines / refund * year`


и замерить время через `%%timeit`:

- цикл: `for i in range(len(df))` + `.iloc`
- `iterrows()`
- `apply(lambda)`
- через Series
- через `.values`

### 3. Оптимизация индексации:

- найти строку по номеру до установки индекса
- установить индекс = CarNumber
- найти строку снова и сравнить время

### 4. Downcasting:

- `df.info(memory_usage='deep')`
- создать копию `optimized`
- уменьшить:
  - `float64 → float32`
  - `int64 → минимально возможный`
- снова `info()` и сравнить память

### 5. Categories:

- перевести object-колонки в category
- сравнить использование памяти

### 6. Очистка памяти:

- `%reset_selective`
- `gc.collect()`
- удалить исходные тяжелые DataFrame

---
