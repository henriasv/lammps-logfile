"""
Regression tests for log files where a run's thermo output is not terminated
by a "Loop time" line (e.g. an interrupted run, or a LAMMPS build that does
not print the loop summary). Such a block ends at "Total wall time", at the
start of the next run, or at end of file. Previously the trailing output was
swallowed into the thermo data as garbage rows, turning numeric columns into
strings.
"""
import io
import os
import tempfile
import unittest

import numpy as np
import pandas as pd

import lammps_logfile
from lammps_logfile import read_log

LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "log.no_loop_time.lammps")

EXPECTED_COLUMNS = ["Time", "PotEng", "KinEng", "Temp", "Press"]
N_ROWS = 32

SECOND_RUN = (
    "Setting up Verlet run ...\n"
    "  Unit style    : lj\n"
    "  Current step  : 3100\n"
    "  Time step     : 0.003\n"
    "Per MPI rank memory allocation (min/avg/max) = 3.416 | 3.416 | 3.416 Mbytes\n"
    "   Step          Temp          Press     \n"
    "      3100   1.0298205     0.83510406   \n"
    "      3200   1.01          0.80         \n"
    "      3300   1.02          0.81         \n"
)


def two_run_log_text():
    """The fixture with a second run (also without "Loop time") appended
    before the final "Total wall time" line."""
    with open(LOG_PATH) as f:
        text = f.read()
    body, tail = text.rsplit("Total wall time", 1)
    return body + SECOND_RUN + "Total wall time" + tail


class TestNoLoopTimeReadLog(unittest.TestCase):
    def assert_single_run_ok(self, df):
        self.assertEqual(len(df), N_ROWS)
        for col in EXPECTED_COLUMNS:
            self.assertIn(col, df.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]),
                            f"{col} should be numeric, got {df[col].dtype}")
        np.testing.assert_allclose(df["Time"].to_numpy(), np.arange(N_ROWS) * 0.3)
        self.assertAlmostEqual(df["Temp"].iloc[0], 0.65)
        self.assertAlmostEqual(df["Temp"].iloc[-1], 1.0298205)
        self.assertAlmostEqual(df["Press"].iloc[-1], 0.83510406)
        self.assertEqual(set(df["run_num"]), {0})

    def test_read_log_from_path(self):
        self.assert_single_run_ok(read_log(LOG_PATH))

    def test_read_log_from_stream(self):
        with open(LOG_PATH) as f:
            df = read_log(io.StringIO(f.read()))
        self.assert_single_run_ok(df)

    def assert_two_runs_ok(self, df):
        self.assertEqual(sorted(df["run_num"].unique()), [0, 1])
        for col in EXPECTED_COLUMNS + ["Step"]:
            self.assertTrue(pd.api.types.is_numeric_dtype(df[col]),
                            f"{col} should be numeric, got {df[col].dtype}")

        run0 = df[df["run_num"] == 0]
        self.assertEqual(len(run0), N_ROWS)
        self.assertAlmostEqual(run0["Temp"].iloc[-1], 1.0298205)
        self.assertTrue(run0["Step"].isna().all())

        run1 = df[df["run_num"] == 1]
        self.assertEqual(len(run1), 3)
        np.testing.assert_array_equal(run1["Step"].to_numpy(), [3100, 3200, 3300])
        np.testing.assert_allclose(run1["Press"].to_numpy(), [0.83510406, 0.80, 0.81])
        self.assertTrue(run1["Time"].isna().all())

    def test_two_runs_from_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "log.lammps")
            with open(path, "w") as f:
                f.write(two_run_log_text())
            self.assert_two_runs_ok(read_log(path))

    def test_two_runs_from_stream(self):
        self.assert_two_runs_ok(read_log(io.StringIO(two_run_log_text())))


class TestNoLoopTimeFile(unittest.TestCase):
    def setUp(self):
        self.log = lammps_logfile.File(LOG_PATH)

    def test_single_run(self):
        self.assertEqual(self.log.get_num_partial_logs(), 1)
        self.assertListEqual(self.log.get_keywords(), sorted(EXPECTED_COLUMNS))

    def test_values_are_numeric(self):
        for col in EXPECTED_COLUMNS:
            data = self.log.get(col)
            self.assertEqual(len(data), N_ROWS)
            self.assertTrue(np.issubdtype(data.dtype, np.number),
                            f"{col} should be numeric, got {data.dtype}")
        np.testing.assert_allclose(self.log.get("Time"), np.arange(N_ROWS) * 0.3)
        self.assertAlmostEqual(self.log.get("Temp")[-1], 1.0298205)
        self.assertAlmostEqual(self.log.get("Press")[-1], 0.83510406)

    def test_two_runs(self):
        log = lammps_logfile.File(io.StringIO(two_run_log_text()))
        self.assertEqual(log.get_num_partial_logs(), 2)
        self.assertListEqual(log.get_keywords(run_num=0), sorted(EXPECTED_COLUMNS))
        self.assertListEqual(log.get_keywords(run_num=1), sorted(["Step", "Temp", "Press"]))
        self.assertEqual(len(log.get("Temp", 0)), N_ROWS)
        self.assertAlmostEqual(log.get("Temp", 0)[-1], 1.0298205)
        np.testing.assert_array_equal(log.get("Step", 1), [3100, 3200, 3300])
        self.assertTrue(np.issubdtype(log.get("Temp", 1).dtype, np.number))


if __name__ == '__main__':
    unittest.main()
