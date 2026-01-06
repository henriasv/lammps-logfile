import unittest
import pandas as pd
from lammps_logfile import read_log

class TestReadLog(unittest.TestCase):
    def test_read_log(self):
        filename = "tests/data/log.lammps"
        df = read_log(filename)

        # Verify total rows
        # From previous manual inspection: run 0 (5 rows), run 1 (5 rows), run 2 (97 rows?)
        # Wait, let's recheck the counts from reproduce_issue.py
        # reproduce_issue.py said:
        # Partial log 0 keys: Step, Time, Temp, Pxx, Pyy, CPULeft (length 5)
        # Partial log 1 keys: Step, Time, Temp, Pxx, Pyy, Press, CPULeft (length 5)
        # Partial log 2 keys: Step, Temp, Pxx, Pyy, CPULeft (length 5... wait, reproduce_issue.py output was truncated or I misread?)
        # In reproduce_issue.py output:
        # Partial log 2 keys: ...
        # Combined DataFrame ... Total rows: 107.
        # So 5 + 5 + 97? Let's check log.lammps again carefully.
        # Run 1: 0 to 400 (step 100) -> 5 rows.
        # Run 2: 5000 to 5400 (step 100) -> 5 rows.
        # Run 3: 10000 to 10400 (step 100) -> 5 rows.
        # Wait, the log file has much more data.

        # Let's read log.lammps content again to be sure.
        # The first run goes from 0 to 5000 with thermo 100 -> 51 rows.
        # The second run goes from 5000 to 10000 with thermo 100 -> 51 rows.
        # The third run goes from 10000 to 10400 with thermo 100 -> 5 rows.
        # Total = 51 + 51 + 5 = 107 rows.

        self.assertEqual(len(df), 107)

        # Verify columns
        expected_columns = {'Step', 'Time', 'Temp', 'Pxx', 'Pyy', 'Press', 'CPULeft', 'run_num'}
        self.assertTrue(expected_columns.issubset(set(df.columns)))

        # Verify run_num
        self.assertEqual(set(df['run_num'].unique()), {0, 1, 2})

        # Verify specific data points
        # Run 0 should not have 'Press' (based on reproduce_issue.py output, wait, let's check log file)
        # Run 0 header: step time temp pxx pyy cpuremain (No Press)
        # Run 1 header: step time temp pxx pyy press cpuremain (Has Press)
        # Run 2 header: step temp pxx pyy cpuremain (No Press, No Time)

        # Check run 0 (first 51 rows)
        run0 = df[df['run_num'] == 0]
        self.assertEqual(len(run0), 51)
        self.assertTrue(pd.isna(run0.iloc[0]['Press']))

        # Check run 1
        run1 = df[df['run_num'] == 1]
        self.assertEqual(len(run1), 51)
        self.assertFalse(pd.isna(run1.iloc[0]['Press']))

        # Check run 2
        run2 = df[df['run_num'] == 2]
        self.assertEqual(len(run2), 5)
        self.assertTrue(pd.isna(run2.iloc[0]['Press']))
        # 'Time' is missing in Run 2 header "step temp pxx pyy cpuremain"
        # However, looking at the log file:
        # thermo_style custom step temp pxx pyy cpuremain
        # So yes, 'Time' should be NaN for run 2.
        self.assertTrue(pd.isna(run2.iloc[0]['Time']))

if __name__ == '__main__':
    unittest.main()
