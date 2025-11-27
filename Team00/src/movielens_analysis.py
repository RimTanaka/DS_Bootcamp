#!/usr/bin/env python3
"""
Модуль для работы с датасетом MovieLens.

Содержит классы для работы с файлами рейтингов, тегов, фильмов и ссылок на внешние источники.
"""

import csv
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from links import Links
from movies import Movies
from ratings import Ratings
from tags import Tags
