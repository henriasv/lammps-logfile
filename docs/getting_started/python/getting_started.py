import lammps_logfile
import matplotlib.pyplot as plt

# Read the log file using the new read_log function
data = lammps_logfile.read_log("../../../examples/logfiles/crack_log.lammps")

# The data is returned as a pandas DataFrame
# We can access columns directly by name
t = data["Time"]
temp = data["Temp"]

plt.figure()
plt.plot(t, temp)
plt.xlabel("Time (ps)")
plt.ylabel("Temperature (K)")
plt.ylim([215, 225])
plt.savefig("time_temp.png")

# Calculate running average using pandas rolling window
# Since pandas DataFrame makes this easy, we don't strictly need a helper,
# but we can show how to do it with pandas
temp_avg = temp.rolling(window=100).mean()

plt.figure()
plt.plot(t, temp, label='Raw')
plt.plot(t, temp_avg, label='Average')
plt.xlabel("Time (ps)")
plt.ylabel("Temperature (K)")
plt.ylim([215, 225])
plt.legend()
plt.savefig("time_temp_avg.png")

# Print available columns
print(data.columns.tolist())
