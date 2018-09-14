from unittest import TestCase
import numpy as np
import os 

import lammps_logfile

class TestFileWithLogFile(TestCase):
    """Test whether the readings from a supplied log file are correct. Requires the supplied file log.lammps.  
    """
    def setUp(self):
        self.log = lammps_logfile.File(os.path.join(os.path.dirname(__file__), "data", "log.lammps"))

    def test_num_entries(self):
        self.assertEqual(self.log.get_num_partial_logs(), 3)

    def test_len_partial_logs(self):
        step = self.log.get("Step", -1)
        self.assertEqual(len(step), 5)
        step = self.log.get("Step", 0)
        self.assertEqual(len(step), 51)
        step = self.log.get("Step", 1)
        self.assertEqual(len(step), 51)
        step = self.log.get("Step", 2)
        self.assertEqual(len(step), 5)

    def test_keyword_partial_logs(self):
        keyword0 = ["Step", "Time", "Temp", "Pxx", "Pyy", "CPULeft"]
        for keyword in keyword0:
            self.assertIsNotNone(self.log.get(keyword, 0))
        self.assertIsNone(self.log.get("Press", 0))

        keyword1 = ["Step", "Time", "Temp", "Pxx", "Pyy", "Press", "CPULeft"]
        for keyword in keyword1:
            self.assertIsNotNone(self.log.get(keyword, 1))

        keyword2 = ["Step", "Temp", "Pxx", "Pyy", "CPULeft"]
        for keyword in keyword2:
            self.assertIsNotNone(self.log.get(keyword, 2))
        self.assertIsNone(self.log.get("Press", 2))
        self.assertIsNone(self.log.get("Time", 2))

    def test_step_entries_contents(self):
        np.testing.assert_equal(self.log.get("Step", 0), np.arange(0,5001, 100))
        np.testing.assert_equal(self.log.get("Step", 1), np.arange(5000,10001, 100))
        np.testing.assert_equal(self.log.get("Step", 2), np.arange(10000,10401, 100))

    def test_get_keywords(self):
        self.assertListEqual(self.log.get_keywords(), sorted(["Step", "Temp", "Pxx", "Pyy", "CPULeft"]))
        self.assertListEqual(self.log.get_keywords(run_num=0), sorted(["Step", "Time", "Temp", "Pxx", "Pyy", "CPULeft"]))
        self.assertListEqual(self.log.get_keywords(run_num=1), sorted(["Step", "Time", "Temp", "Pxx", "Pyy", "Press", "CPULeft"]))
        self.assertListEqual(self.log.get_keywords(run_num=2), sorted(["Step", "Temp", "Pxx", "Pyy", "CPULeft"]))