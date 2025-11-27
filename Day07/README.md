# День X — Data Visualization (SQL + Pandas + Matplotlib + Seaborn + Plotly)

---

# Exercise 00 — Line chart

**Папка:** `ex00/`  
**Файл:** `00_line_chart.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Подключиться к базе (та же база, что и на прошлый день).
2. Выполнить SQL-запрос:
   - выбрать `datetime` из `pageviews`
   - только пользователи (`uid LIKE 'user_%'`)
3. На основе полученных данных:
   - сгруппировать по **дате**
   - посчитать количество посещений в день
4. Построить график через `.plot()`:
   - размер шрифта: `fontsize=8`
   - размер фигуры: `(15, 8)`
   - заголовок: **Views per day**
   - повернуть xticks (как в примерах)
5. Закрыть подключение.

---

# Exercise 01 — Line chart with styles

**Папка:** `ex01/`  
**Файл:** `01_line_chart_styles.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Анализировать только пользователей (без админов).
2. Взять только те даты, когда **есть и просмотры, и коммиты**.
3. Построить график, **идентичный примеру**:
   - две линии: просмотры и коммиты
   - одинаковый стиль
   - шрифт 8
   - размер `(15,8)`
4. В конце ноутбука добавить markdown-вопрос:

```
"How many times was the number of views larger than 150?"
The answer is ___
```


---

# Exercise 02 — Bar chart

**Папка:** `ex02/`  
**Файл:** `02_bar_chart.ipynb`  
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Только пользователи.
2. Определить время суток:
- night: 00:00–03:59  
- morning: 04:00–09:59  
- afternoon: 10:00–16:59  
- evening: 17:00–23:59  
3. Построить bar chart (любая приятная палитра).
4. Размер фигуры и шрифта — как всегда `(15,8)` и `fontsize=8`.
5. В конце ноутбука Markdown с вопросами:

```
“When do our users usually commit the labs: in the night, morning, afternoon, or evening?”
→ ответ: два самых популярных периода

“Which day has:
• the most number of commits
• and at the same time, commits in the evening > commits in the afternoon?”
→ ответ: дата
```


---

# Exercise 03 — Bar charts (Workday vs Weekend)

**Папка:** `ex03/`
**Файл:** `03_bar_charts.ipynb`
**Импорты:** `pandas`, `sqlite3`

### Требования

1. Только пользователи.
2. Для каждого часа вычислить:
- среднее число коммитов в рабочие дни
- среднее число коммитов на выходных
(пустые часы не учитывать)
3. Построить bar chart (любая палитра).
4. Размер и шрифт — как всегда.
5. В конце Markdown:

```
“Is the dynamic different on working days and weekends?”
→ указать:
• час максимума в рабочие дни
• час максимума на выходных
```

---

# Exercise 04 — Histogram

**Папка:** `ex04/`
**Файл:** `04_histogram.ipynb`
**Импорты:** `pandas`, `sqlite3`, `matplotlib.pyplot`

### Требования

1. Только пользователи.
2. Создать два списка:
- значения коммитов по часам в рабочие дни
- значения коммитов по часам в выходные
3. Построить два histogram:
- общие оси
- прозрачность front-гистограммы: `alpha=0.7`
- figsize `(15,8)`
3. Финальный Markdown:


```
“Are there hours when the total number of commits was higher on weekends than on working days?”
→ вывести топ-4 часов
```


---

# Exercise 05 — Boxplot

**Папка:** `ex05/`  
**Файл:** `05_boxplot.ipynb`  
**Импорты:** `pandas`, `sqlite3`, `matplotlib.pyplot`

### Требования

1. Загрузить данные (использовать datamart/test-control из прошлых дней).
2. При необходимости преобразовать данные.
3. Построить boxplot:
- палитра такая же, как в примере
- figsize `(15,8)`
- title fontsize = 15
- ширина линий box = 3
- ширина median = 2
4. В конце Markdown:


```
“What was the IQR of the control group before the newsfeed?”
→ округлить на глаз до ближайших 10
```


---

# Exercise 06 — Scatter Matrix

**Папка:** `ex06/`
**Файл:** `06_scatter_matrix.ipynb`
**Импорты:** `pandas`, `sqlite3`, `scatter_matrix`

### Требования

1. Создать dataframe, содержащий по каждому пользователю:
- avg_diff (без project1)
- pageviews
- commits (из checker)
2. Построить scatter matrix:
- figsize `(15,8)`
- точек size = 200
- ширина линий диагональных kde = 3
- палитра любая
3. Добавить финальный Markdown с вопросами:


```
Can we say low pageviews → low commits? (yes/no)

Can we say low pageviews → small avg diff? (yes/no)

Are there many users with a low number of commits and few with a high number? (yes/no)

Are there many users with a small avg diff and few with a large avg diff? (yes/no)
```


---

# Exercise 07 — Heatmap (Bonus)

**Папка:** `ex07/`
**Файл:** `07_heatmap.ipynb`
**Импорты:** `pandas`, `sqlite3`, `matplotlib`, `make_axes_locatable`

### Требования

1. Только пользователи.
2. Использовать таблицу `checker`.
3. Строим два heatmap:
- commits per weekday
- commits per hour per user
4. Использовать абсолютные значения (не средние).
5. Отсортировать DataFrame по сумме коммитов.
6. В конце Markdown:

```

“Which user has the most commits on Tue?” → user_*
“Which user has the most commits on Thu?” → user_*
“On which weekday do users commit the least?” → weekday
“Which user and hour correspond to the max commits?” → user_*, hour
```


---

# Exercise 08 — Seaborn

**Папка:** `ex08/`  
**Файл:** `08_seaborn.ipynb`  
**Импорты:** `pandas`, `sqlite3`, `matplotlib`, `seaborn`

### Требования

1. Только пользователи.
2. Использовать `checker` со статусом `ready`.
3. Фильтровать только `project1`.
4. Построить линейный график Seaborn:
- linewidth = 3
- фон графика — серый
- высота = 10, ширина = 15
- title fontsize = 30
- axis label fontsize = 15
5. В конце Markdown:

```
“Which user was the leader most of the time?” → user_*
“Which user was the leader only briefly?” → user_*
```


---

# Exercise 09 — Plotly (Animation)

**Папка:** `ex09/`  
**Файл:** `09_plotly.ipynb`  
**Импорты:** `pandas`, `sqlite3`, `plotly.graph_objects`, `numpy`

### Требования

1. Анализ как в предыдущем упражнении (только project1, пользователи).
2. Построить **анимированный график**:
- аналог предыдущего Seaborn-графика
- но в Plotly
- со сменой кадров по времени
3. Использовать Plotly reference-гайд (дан ссылкой в условии).

---





