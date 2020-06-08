About lammps-logfile
========================
:code:`lammps-logfile` is a lightweight package for reading time-series data from LAMMPS log files. 

Basic usage to get and plot the temperature in a simulation as a function of time is: 

.. code-block:: python 

    import lammps_logfile

    log = lammps_logfile.File("log.lammps")

    x = log.get("Time")
    y = log.get("Temp")

    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.show()


