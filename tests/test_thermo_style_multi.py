import unittest
import pandas as pd
import os
from lammps_logfile import read_log

class TestThermoStyleMulti(unittest.TestCase):
    def test_read_multi_log(self):
        log_path = "examples/simulations/01_fcc_thermo_multi/out/log.lammps"

        # Ensure file exists
        self.assertTrue(os.path.exists(log_path), f"Log file not found at {log_path}")

        df = read_log(log_path)

        # Check if DataFrame is not empty
        self.assertFalse(df.empty, "DataFrame should not be empty for thermo_style multi")

        # Check for expected columns (Thermo keys)
        expected_cols = ["Step", "TotEng", "KinEng", "Temp", "PotEng", "Press"]
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Column {col} missing from DataFrame")

        self.assertGreater(len(df), 0)
        self.assertIn('run_num', df.columns)
        self.assertEqual(df['run_num'].nunique(), 3)

    def test_read_mixed_log(self):
        log_path = "examples/simulations/04_bcc_multi_then_custom/out/log.lammps"

        # Ensure file exists
        self.assertTrue(os.path.exists(log_path), f"Log file not found at {log_path}")

        df = read_log(log_path)

        self.assertFalse(df.empty, "DataFrame should not be empty")

        expected_cols = ["Step", "TotEng", "Temp", "PotEng", "Press", "Volume", "v_rho"]
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Column {col} missing from DataFrame")

        unique_runs = df['run_num'].nunique()
        self.assertGreaterEqual(unique_runs, 3, f"Expected at least 3 runs, found {unique_runs}")

        # Check specific values to ensure mixed parsing worked
        # Run 0 (multi) should have Step=0
        run0 = df[df['run_num'] == 0]
        self.assertFalse(run0.empty)

        # Run with custom style should have v_rho
        self.assertTrue(df['v_rho'].notna().any(), "v_rho should be present in some rows")

        # And rows from multi style (run 0) should have NaN for v_rho (since it wasn't in multi output)
        # Note: Depending on pandas version and concat, it might be NaN.
        # Let's verify run 0 specifically.
        # In this log, Run 0 is multi. It does NOT have v_rho.
        self.assertTrue(run0['v_rho'].isna().all(), "v_rho should be NaN for the first multi run")

if __name__ == '__main__':
    unittest.main()
