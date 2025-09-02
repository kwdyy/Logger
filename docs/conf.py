# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Logger'
copyright = '2025, kwdyy'
author = 'kwdyy'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # ✅ コードのdocstringを自動抽出
    'sphinx.ext.viewcode',     # ✅ ソースコードへのリンク
    'sphinx.ext.napoleon',     # ✅ GoogleスタイルやNumPyスタイルのdocstring対応
    'myst_parser',             # ✅ Markdown対応
]

source_suffix = {
    '.rst': None,
    '.md': None,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # logger.py がルートにあるため
