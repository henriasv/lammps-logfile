import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lammps-logfile',
      version='1.0.2',
      description='Tool to read lammps log files into python data structure',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/henriasv/lammps-logfile',
      author='Henrik Andersen Sveinsson',
      author_email='henrik.sveinsson@me.com',
      license='GNU GPL v3.0',
      packages=setuptools.find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=['pandas', 'numpy', 'matplotlib'],
      entry_points={
        'console_scripts': [
            'lammps_logplotter=lammps_logfile.cmd_interface:run'
        ]
      },
      zip_safe=False)
