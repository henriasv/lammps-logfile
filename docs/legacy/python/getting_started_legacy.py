from lammps_logfile import File

log = File("../../../examples/logfiles/crack_log.lammps")

t = log.get("Time")
temp = log.get("Temp")

import matplotlib.pyplot as plt

plt.plot(t, temp)
plt.xlabel("Time (ps)")
plt.ylabel("Temperature (K)")
plt.ylim([215, 225])
plt.savefig("time_temp.png")

from lammps_logfile import running_mean

temp_avg = running_mean(temp, 100)

plt.plot(t, temp_avg)
plt.xlabel("Time (ps)")
plt.ylabel("Temperature (K)")
plt.ylim([215, 225])
plt.savefig("time_temp_avg.png")

print(log.get_keywords())
