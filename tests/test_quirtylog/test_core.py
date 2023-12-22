"""
------------
test_core.py
------------

Test the core module

To run the code
$ python test_core.py
"""
import unittest
from uuid import uuid4
import shutil
from pathlib import Path
from test_quirtylog.config import xml_test_folder
from quirtylog.core import retrieve_name, check_path, create_logger
from logging import Logger


class TestRetrieveName(unittest.TestCase):
    """Test the retrieve_name function"""

    def test_str(self):
        """Test a str variable"""

        var = 'x'
        name = retrieve_name(var=var)
        self.assertEqual(name, 'var')

    def test_list(self):
        """Test a list variable"""

        values = [1, 2, 3]
        name = retrieve_name(var=values)
        self.assertEqual(name, 'values')


class TestCheckPath(unittest.TestCase):
    """Test the check_path function"""

    def test_str(self):
        """Test a str object"""
        p = 'src/'
        out = check_path(p, name='p')
        self.assertIsInstance(out, Path)

    def test_path(self):
        """Test a Path object"""
        p = Path('src/')
        out = check_path(p, name='p')
        self.assertIsInstance(out, Path)

    def test_float(self):
        """Test a float object"""
        n = 1.2

        with self.assertRaises(TypeError):
            _ = check_path(n, name='n')


class ABCTestLogger(unittest.TestCase):
    """Base class for logger tests"""

    @classmethod
    def setUpClass(cls):
        """Set the test context"""

        cls.log_folder = Path('logs/').absolute()
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)

        cls.log_folder.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean the test context"""

        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)


class TestCreateLogger(ABCTestLogger):
    """Test the create_logger function"""

    def _assert_logs(self, logger: Logger, expected_name: str):
        message = str(uuid4())
        for method, name in \
                [('info', 'info'), ('debug', 'debug'), ('warning', 'warn'), ('error', 'errors')]:
            f = getattr(logger, method)
            f(message)

            filename = self.log_folder / f'{name}.log'

            self.assertTrue(filename.exists(), f'{filename} not exists')
            with open(filename, 'r') as f:
                content = f.read()

            self.assertIn(message, content)
            self.assertIn(expected_name, content)

            filename.unlink(missing_ok=True)

        # assert all files are removed
        files = list(self.log_folder.glob('*'))
        self.assertEqual(len(files), 0)

    def test_create_simple_logger(self):
        """Test the function with default options"""

        lgr = create_logger(log_path=self.log_folder)

        self.assertIsInstance(lgr, Logger)

        self._assert_logs(logger=lgr, expected_name='test_core')

    def test_create_named_logger(self):
        """Test the function with default options"""

        lgr = create_logger(log_path=self.log_folder, name='totti')

        self.assertIsInstance(lgr, Logger)

        self._assert_logs(logger=lgr, expected_name='totti')


def build_suite():
    """Build the TestSuite"""
    suite = unittest.TestSuite()

    suite.addTest(TestRetrieveName('test_str'))
    suite.addTest(TestRetrieveName('test_list'))

    suite.addTest(TestCheckPath('test_str'))
    suite.addTest(TestCheckPath('test_path'))
    suite.addTest(TestCheckPath('test_float'))

    suite.addTest(TestCreateLogger('test_create_simple_logger'))
    suite.addTest(TestCreateLogger('test_create_named_logger'))

    return suite


if __name__ == '__main__':
    """The main script"""

    runner = unittest.TextTestRunner(failfast=True, output=xml_test_folder)
    runner.run(build_suite())
