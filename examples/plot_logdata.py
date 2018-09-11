import os
import matplotlib.pyplot as plt

import lammps_logfile

log = lammps_logfile.File(os.path.join(os.path.dirname(__file__), "logfiles", "crack_log.lammps"))

x = log.get("Time")
y = log.get("Pyy")

plt.figure(figsize=(6,6))
plt.subplot(221)
plt.plot(x, y)
plt.xlabel("$t$")
plt.ylabel("$p_{yy}$")

plt.subplot(222)
for i in range(log.get_num_partial_logs()):
    x = log.get("Time", run_num=i)
    y = log.get("Pyy", run_num=i)
    plt.plot(x, y)
    plt.xlabel("$t$")
    plt.ylabel("$p_{yy}$")

plt.subplot(223)
x = log.get("Time")
y = log.get("Temp")
plt.plot(x, y)
plt.xlabel("$t$")
plt.ylabel("$T$")

plt.subplot(224)
for i in range(log.get_num_partial_logs()):
    x = log.get("Time", run_num=i)
    y = log.get("Temp", run_num=i)
    plt.plot(x, y)
    plt.xlabel("$t$")
    plt.ylabel("$T$")
plt.tight_layout()
plt.show()

