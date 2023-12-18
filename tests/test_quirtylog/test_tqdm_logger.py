"""
-------------------
test_tqdm_logger.py
-------------------

This test check the tqdm module

To run the code
$ python test_tqdm_logger.py
"""
import tqdm
import time
import unittest
import logging
import xmlrunner
from pathlib import Path
from joblib import delayed, Parallel
from config import xml_test_folder


from quirtylog.tqdm_logger import TqdmToLogger



class TestTqdmToLogger(unittest.TestCase):
    """The base class for TqdmToLogger test"""

    @classmethod
    def setUpClass(cls):
        """Configure the test"""

        cls.logname = Path(__file__).absolute().parent / 'log.info'
        if cls.logname.exists():
            cls.logname.unlink()
        logging.basicConfig(
            filename=cls.logname,
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO
        )

        cls.logger = logging.getLogger(cls.__name__)
        cls.tqdm_out = TqdmToLogger(cls.logger, level=logging.INFO)

        cls.n_rows = 10

    def test_tqdm(self):
        """Test the tqdm logger"""

        for _ in tqdm.tqdm(range(self.n_rows), file=self.tqdm_out):
            time.sleep(.1)

        num_lines = sum(1 for _ in open(self.logname))
        self.assertEqual(num_lines, self.n_rows + 2)  # here we count 0 and 100

    def test_joblib_parallel(self):
        """Test the tqdm logger inside a joblib execution"""

        _ = Parallel(n_jobs=2)(
            delayed(lambda x: x + 1)(i ** 2)
            for i in tqdm.tqdm(range(self.n_rows), file=self.tqdm_out)
        )

        num_lines = sum(1 for _ in open(self.logname))
        self.assertGreater(num_lines, self.n_rows + 2)  # here we count 0 and 100
        self.assertLessEqual(num_lines, 2 * (self.n_rows + 2))  # here we count 0 and 100

    @classmethod
    def tearDownClass(cls):
        """The tear down procedure"""
        if cls.logname.exists():
            cls.logname.unlink()


def build_suite():
    """Build the TestSuite"""
    suite = unittest.TestSuite()
    suite.addTest(TestTqdmToLogger('test_tqdm'))
    suite.addTest(TestTqdmToLogger('test_joblib_parallel'))

    return suite


if __name__ == '__main__':
    """The main script"""

    runner = xmlrunner.XMLTestRunner(output=xml_test_folder)
    runner.run(build_suite())
