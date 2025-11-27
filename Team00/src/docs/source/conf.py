# Configuration file for the Sphinx documentation builder.

import os
import sys

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'MovieLens Analyzer'
copyright = '2025, Weaverir'
author = 'Weaverir'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "style_external_links": True,
}
