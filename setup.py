import setuptools
from setuptools import setup

setup(name='lammps-logfile',
      version='0.1',
      description='Tool to read lammps log files into python data structure',
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
