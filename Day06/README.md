# SQL + Pandas — Техническое задание (короткое)

---

# Exercise 00 — Select

**Папка:** `ex00/`  
**Файл:** `ex00_first_select.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Положить SQLite-базу в `src/data/`.
2. Создать подключение через `sqlite3.connect()`.
3. Получить схему таблицы `pageviews`:
   - `PRAGMA table_info(pageviews);`
4. Вывести первые 10 строк таблицы.
5. Сформировать выборку **одним SQL-запросом**:
   - оставить только колонки: `uid`, `datetime`
   - выбрать только пользователей `uid LIKE 'user_%'` (исключить админов)
   - отсортировать по `uid` по возрастанию
   - `datetime` сделать индексом
   - привести `datetime` к `DatetimeIndex`
   - сохранить в `pageviews`
6. Закрыть соединение.

---

# Exercise 01 — Subquery

**Папка:** `ex01/`  
**Файл:** `ex01_subquery.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Подключиться к базе.
2. Получить схему таблицы `checker`.
3. Вывести первые 10 строк.
4. Одним SQL-запросом (разрешены подзапросы) подсчитать количество строк, где:

   - `status = 'ready'`
   - `numTrials = 1`
   - `labname IN ('laba04','laba04s','laba05','laba06','laba06s','project1')`
   - берутся только `uid` из `pageviews` (**INNER** логика)

5. Сохранить результат в DataFrame с колонкой `cnt`.
6. Закрыть соединение.

---

# Exercise 02 — Join (Datamart)

**Папка:** `ex02/`  
**Файл:** `ex02_joins.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

Создать витрину (`datamart`) **одним SQL-запросом**, соединив `pageviews` и `checker`.

Таблица должна содержать:

- `uid`
- `labname`
- `first_commit_ts` (переименованный `timestamp` из `checker`)
- `first_view_ts` (первая дата просмотра newsfeed-а из `pageviews`)

### Условия:

- фильтр: `status='ready'`
- фильтр: `numTrials=1`
- фильтр по лабам: laba04, laba04s, laba05, laba06, laba06s, project1
- `uid LIKE 'user_%'`
- `first_commit_ts` и `first_view_ts` → `datetime64[ns]`

### После SQL:

- создать DataFrame `test`: строки, где `first_view_ts` **не пустой**
- создать DataFrame `control`: где `first_view_ts` **пустой**
- заполнить пропуски в `control.first_view_ts` средним временем из тестовой группы
- сохранить `test` и `control` обратно в базу
- закрыть соединение

---

# Exercise 03 — Aggregations

**Папка:** `ex03/`  
**Файл:** `ex03_aggs.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Задачи

1. Подключение.
2. Получить схему таблицы `test`.
3. Показать первые 10 строк.

### 1 Минимальный delta (commit - deadline)

- Посчитать **одним SQL-запросом**
- исключить `project1`
- вернуть:
  - `uid`
  - минимальный `delta_hours`
- сохранить в DataFrame `df_min`

### 2 Максимальный delta

- аналогично  
- DataFrame `df_max`

### 3 Средний delta

- аналогично  
- но **без колонки `uid`**  
- DataFrame `df_avg`

### 4 Корреляция Pageviews ↔ Delta

- Одним SQL-запросом создать таблицу:

| uid | avg_diff | pageviews |

- `avg_diff` — средняя разница commit–deadline по пользователю  
- `pageviews` — число посещений newsfeed  
- исключить `project1`
- сохранить в DataFrame `views_diff`

- Вычислить корреляцию: `views_diff.corr()`




Закрыть соединение.

---

# Exercise 04 — A/B Testing

**Папка:** `ex04/`
**Файл:** `ex04_ab-test.ipynb`
**Импорты:** `pandas`, `sqlite3`

### Цель

Проверить гипотезу:
**после просмотра Newsfeed студенты начинают делать первые коммиты раньше сроков?**

### Задачи

1. Подключение.

2. Одним SQL-запросом для каждой группы (test, control) получить:

 DataFrame `test_results`:

 | time   | avg_diff |
 |--------|----------|
 | before | …        |
 | after  | …        |

 DataFrame `control_results` — аналогично.

 Условия:
 - исключить `project1`
 - учитывать только тех пользователей, у кого есть данные **и до, и после** точки `first_view_ts`

3. Закрыть соединение.

4. Ответить на вопрос:
 **Подтвердилась ли гипотеза и влияет ли Newsfeed-страница на поведение студентов?**

---


