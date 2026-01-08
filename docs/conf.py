# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'lammps-logfile'
copyright = '2020, Henrik Andersen Sveinsson'
author = 'Henrik Andersen Sveinsson'
version = '1.1.2'
release = '1.1.3'

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinxarg.ext",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
    "sphinx_design",
]
add_module_names = False 

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Intersphinx Configuration -----------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'

html_theme_options = {
    "source_repository": "https://github.com/henriasv/lammps-logfile",
    "source_branch": "master",
    "source_directory": "docs/",
}

html_static_path = ['_static']
html_logo = '_static/logo.svg'
html_favicon = '_static/favicon.png'
html_css_files = ['custom.css']

# -- Sphinx Gallery Configuration --------------------------------------------

from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
     'examples_dirs': 'examples_source',   # path to your example scripts
     'gallery_dirs': 'examples',  # path to where to save gallery generated output
     'filename_pattern': 'plot_',
     'within_subsection_order': FileNameSortKey,
     'download_all_examples': False,
}

# -- MyST Parser Configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
