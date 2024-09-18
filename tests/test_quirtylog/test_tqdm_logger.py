"""
-------------------
test_tqdm_logger.py
-------------------

This test check the tqdm module

To run the code
$ python test_tqdm_logger.py
"""

import time
import shutil
import logging
import unittest

from pathlib import Path

import tqdm
import xmlrunner

from joblib import Parallel, delayed
from test_quirtylog.config import xml_test_folder

from quirtylog import create_logger
from quirtylog.tqdm_logger import TqdmToLogger


def _slow_parallel_function(i):
    time.sleep(1)
    return i + 1


class TestTqdmToLogger(unittest.TestCase):
    """The base class for TqdmToLogger test"""

    @classmethod
    def setUpClass(cls):
        """Configure the test"""

        cls.log_folder = Path().absolute() / "logs"
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)

        cls.log_folder.mkdir(exist_ok=True)
        cls.log_filename = cls.log_folder / "info.log"

        cls.logger = create_logger(log_path=cls.log_folder, name="tqdm-logger")

        cls.tqdm_out = TqdmToLogger(cls.logger, level=logging.INFO)

        cls.n_rows = 10

    def test_tqdm(self):
        """Test the tqdm logger"""

        for i in tqdm.tqdm(range(self.n_rows), file=self.tqdm_out):
            _slow_parallel_function(i)

        self.assertTrue(self.log_filename.exists())
        num_lines = sum(1 for _ in open(self.log_filename))
        self.assertEqual(num_lines, self.n_rows + 2)  # here we count 0 and 100

    def test_joblib_parallel(self):
        """Test the tqdm logger inside a joblib execution"""

        _ = Parallel(n_jobs=2)(
            delayed(_slow_parallel_function)(i**2)
            for i in tqdm.tqdm(range(self.n_rows), file=self.tqdm_out)
        )

        self.assertTrue(self.log_filename.exists())
        num_lines = sum(1 for _ in open(self.log_filename))
        self.assertGreater(num_lines, self.n_rows + 2)  # here we count 0 and 100
        self.assertLessEqual(num_lines, 2 * (self.n_rows + 2))  # here we count 0 and 100

    @classmethod
    def tearDownClass(cls):
        """Execute the tear down procedure"""
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)


def build_suite():
    """Build the TestSuite"""
    suite = unittest.TestSuite()

    suite.addTest(TestTqdmToLogger("test_tqdm"))
    suite.addTest(TestTqdmToLogger("test_joblib_parallel"))

    return suite


if __name__ == "__main__":
    """The main script"""

    runner = xmlrunner.XMLTestRunner(output=xml_test_folder)
    runner.run(build_suite())
