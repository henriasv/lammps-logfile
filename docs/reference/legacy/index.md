# Legacy Documentation

This section describes the legacy interface using the `File` class. This interface is maintained for backward compatibility.

## Getting log data

```{literalinclude} python/getting_started_legacy.py
:lines: 1-6
```

Now the arrays `t` and `temp` contain the log data corresponding to the `Time` and `Temp` columns in the log file.

## Plotting log data

```{literalinclude} python/getting_started_legacy.py
:lines: 8-14
```

To make the plot pop up in a window rather than being saved to a file, run `plt.show()` rather than `plt.savefig(...)`.

```{figure} python/time_temp.png
:scale: 100 %
:alt: Plot of temperature vs. time

Plot of temperature vs. time
```

## Running average

```{literalinclude} python/getting_started_legacy.py
:lines: 16-24
```

```{figure} python/time_temp_avg.png
:scale: 100 %
:alt: Plot of temperature vs. time

Plot of temperature vs. time. The blue curve is the raw output, whereas in the orange curve the temperature has been smoothed over a 100 log entries wide averaging window.
```

## What data are available in the log file?

To inspect what columns are available, you can run the `get_keywords`-method on the `File` object:

```python
print(log.get_keywords())
```

This command yields an output like the one below, which shows what columns we may `get` from the `File` object:

```{literalinclude} python/legacy_output.txt
```
