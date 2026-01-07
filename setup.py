import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lammps-logfile',
      version='1.1.1',
      description='Tool to read lammps log files into python data structure',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/henriasv/lammps-logfile',
      author='Henrik Andersen Sveinsson',
      author_email='henrik.sveinsson@me.com',
      license='GNU GPL v3.0',
      packages=setuptools.find_packages(),
      install_requires=['pandas', 'numpy', 'matplotlib'],
      extras_require={
          'docs': [
              'sphinx',
              'furo',
              'sphinx-gallery',
              'myst-parser',
              'sphinx-copybutton',
              'sphinx-design',
              'sphinx-argparse',
          ]
      },
      entry_points={
        'console_scripts': [
            'lammps_logplotter=lammps_logfile.cmd_interface:run'
        ]
      },
      zip_safe=False,
      python_requires='>=3.8',
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
      ])
