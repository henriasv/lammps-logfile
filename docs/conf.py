# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'lammps-logfile'
copyright = '2020, Henrik Andersen Sveinsson'
author = 'Henrik Andersen Sveinsson'

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
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

# -- Options for HTML output -------------------------------------------------

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/henriasv/lammps-logfile",
            "icon": "fa-brands fa-github",
        },
    ],
    "show_toc_level": 2,
    "navbar_align": "left",  # Adjust navbar alignment
}

# -- Sphinx Gallery Configuration --------------------------------------------

from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
     'examples_dirs': 'examples_source',   # path to your example scripts
     'gallery_dirs': 'examples',  # path to where to save gallery generated output
     'filename_pattern': 'plot_',
     'within_subsection_order': FileNameSortKey,
}

# -- MyST Parser Configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
