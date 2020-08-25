Getting started
==================

Getting log data
-----------------
    
.. literalinclude:: python/getting_started.py
    :lines: 1-6

Now the arrays :code:`t` and :code:`temp` contain the log data corresponding to the :code:`Time` and :code:`Temp` columns in the log file. 

Plotting log data 
-----------------

.. literalinclude:: python/getting_started.py
    :lines: 8-14 

To make the plot pop up in a window rather than being saved to a file, run `plt.show()` rather than `plt.savefig(...)`. 

.. figure:: python/time_temp.png
   :scale: 100 %
   :alt: Plot of temperature vs. time

   Plot of temperature vs. time


Running average
----------------
.. literalinclude:: python/getting_started.py
    :lines: 16-24
    
.. figure:: python/time_temp_avg.png
   :scale: 100 %
   :alt: Plot of temperature vs. time

   Plot of temperature vs. time. The blue curve is the raw output, whereas in the orange curve the temperature has been smoothed over a 100 log entries wide averaging window. 

What data are available in the log file? 
----------------------------------------
To inspect what columns are available, you can run the `get_keywords`-method on the `File` object:

.. code-block:: python

    print(log.get_keywords())

This command yields an output like the one below, which shows what columns we may :code:`get` from the :code:`File` object:

.. literalinclude:: python/output.txt

Command line tool 
------------------
The following is the help message from the command line tool `lammps_logplotter` that comes with lammps-logplotter. This tool is meant to quicky inspect lammps log files without having to write a python script. 

.. code-block:: bash 
    
    usage: lammps_logplotter [-h] [-x X] [-y Y [Y ...]] [-a RUNNING_AVERAGE] input_file

    Plot contents from lammps log files

    positional arguments:
    input_file            Lammps log file containing thermo output from lammps simulation.

    optional arguments:
    -h, --help            show this help message and exit
    -x X                  Data to plot on the first axis
    -y Y [Y ...]          Data to plot on the second axis. You can supply several names to get several plot lines in the same figure.
    -a RUNNING_AVERAGE, --running_average RUNNING_AVERAGE
                            Optionally average over this many log entries with a running average. Some thermo properties fluctuate wildly, and often we are interested in te
                            running average of properties like temperature and pressure.