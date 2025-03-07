"""
------------
test_core.py
------------

Test the core module

To run the code
$ python test_core.py
"""

import re
import time
import shutil
import logging
import unittest

from uuid import uuid4
from random import randint
from logging import Logger
from pathlib import Path

from test_quirtylog.config import xml_test_folder

from quirtylog.core import (check_path, measure_time, create_logger,
                            retrieve_name, clear_old_logs, configure_logger,
                            display_arguments)


def _mock_bad_func():
    return 1 / 0


class TestRetrieveName(unittest.TestCase):
    """Test the retrieve_name function"""

    def test_str(self):
        """Test a str variable"""

        var = "x"
        name = retrieve_name(var=var)
        self.assertEqual(name, "var")

    def test_list(self):
        """Test a list variable"""

        values = [1, 2, 3]
        name = retrieve_name(var=values)
        self.assertEqual(name, "values")


class TestCheckPath(unittest.TestCase):
    """Test the check_path function"""

    def test_str(self):
        """Test a str object"""
        p = "src/"
        out = check_path(p, name="p")
        self.assertIsInstance(out, Path)

    def test_path(self):
        """Test a Path object"""
        p = Path("src/")
        out = check_path(p, name="p")
        self.assertIsInstance(out, Path)

    def test_float(self):
        """Test a float object"""
        n = 1.2

        with self.assertRaises(TypeError):
            _ = check_path(n, name="n")


class ABCTestLogger(unittest.TestCase):
    """Base class for logger tests"""

    @classmethod
    def setUpClass(cls):
        """Set the test context"""

        cls.log_folder = Path("logs/").absolute()
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)

        cls.log_folder.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean the test context"""

        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)


class ABCAssertLogs(ABCTestLogger):
    """A custom class used to test the output of logging"""

    def _assert_logs(self, logger: Logger, expected_name: str, cases: list | None = None):
        if cases is None:
            cases = [
                ("info", "info"),
                ("debug", "debug"),
                ("warning", "warn"),
                ("error", "errors"),
            ]

        message = str(uuid4())
        for method, name in cases:
            f = getattr(logger, method)
            f(message)

            if name is not None:
                filename = self.log_folder / f"{name}.log"

                self.assertTrue(filename.exists(), f"{filename} not exists")
                with open(filename, "r") as f:
                    content = f.read()

                self.assertIn(message, content)
                self.assertIn(expected_name, content)

                filename.unlink(missing_ok=True)

        # assert all files are removed
        files = list(self.log_folder.glob("*"))
        self.assertEqual(len(files), 0)


class TestConfigureLogger(ABCAssertLogs):
    """Test the configure_logger function"""

    def test_configure_default(self):
        """Test the function using the default option"""

        n = "test-configure-default"
        lgr = logging.getLogger(name=n)
        configure_logger(config_file="default")

        self._assert_logs(logger=lgr, expected_name=n)

    def test_configure_none(self):
        """Test the function using the None option"""

        n = "test-configure-none"
        lgr = logging.getLogger(name=n)
        configure_logger(log_path=self.log_folder, config_file=None)

        cases = [("info", None)]
        self._assert_logs(logger=lgr, expected_name=n, cases=cases)


class TestCreateLogger(ABCAssertLogs):
    """Test the create_logger function"""

    def test_create_simple_logger(self):
        """Test the function with default options"""
        with self.assertRaises(TypeError):
            create_logger(log_path=self.log_folder, remove_old_log=False, name=1)

        lgr = create_logger(log_path=self.log_folder, remove_old_log=False)

        self.assertIsInstance(lgr, Logger)

        self._assert_logs(logger=lgr, expected_name="test_core")

    def test_create_logger_none_path(self):
        """Test the function with default options"""

        lgr = create_logger(log_path=None, remove_old_log=False)

        self.assertIsInstance(lgr, Logger)

        self._assert_logs(logger=lgr, expected_name="test_core")

    def test_create_named_logger(self):
        """Test the function with name defined by user"""

        lgr = create_logger(log_path=self.log_folder, name="totti")

        self.assertIsInstance(lgr, Logger)

        self._assert_logs(logger=lgr, expected_name="totti")

    def test_create_with_none_yaml(self):
        """Test the function with config None"""

        lgr = create_logger(
            log_path=self.log_folder, name="config_none", config_file=None
        )

        self.assertIsInstance(lgr, Logger)
        lgr.info("What")

    def test_create_with_custom_yaml(self):
        """Test the function with config defined by user"""

        log_filename = self.log_folder / "info.log"

        config_content = f"""
        version: 1
        disable_existing_loggers: true
        formatters:
          simple:
            format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        handlers:
          console:
            class: logging.StreamHandler
            level: INFO
            formatter: simple
            stream: ext://sys.stdout
          file:
            class: logging.FileHandler
            level: DEBUG
            filename: {str(log_filename)}
        loggers:
          simpleExample:
            level: DEBUG
            handlers: [console]
            propagate: no
        root:
          level: DEBUG
          handlers: [console,file]
        """

        config_file = Path("config.yaml")
        if config_file.exists():
            config_file.unlink()

        with open(config_file, "w") as f:
            f.write(config_content)

        lgr = create_logger(
            log_path=self.log_folder, config_file=config_file, name="using_config"
        )
        txt = "my_awesome_message"
        lgr.info(txt)

        self.assertTrue(log_filename.exists())

        with open(log_filename, "r") as f:
            content = f.read()

        self.assertEqual(len(content.split("\n")), 2)
        self.assertIn(txt, content)

        if config_file.exists():
            config_file.unlink()

        if log_filename.exists():
            log_filename.unlink()

    def test_create_db(self):
        """Test the function with db option"""

        dbname = "log.db"
        lgr = create_logger(log_path=self.log_folder, db=dbname)
        self.assertIsInstance(lgr, Logger)

        db = self.log_folder / "log.db"
        self.assertTrue(db.exists())

    def test_from_main(self):
        """Test the function with db option"""

        code = f"""
        import quirtylog
        lgr = quirtylog.create_logger(log_path="{self.log_folder}")
        lgr.info("hello")
        """

        code = "\n".join([line.strip() for line in code.split("\n")])
        scope = {}
        exec(code, scope)

        log_filename = self.log_folder / "info.log"
        with open(log_filename, "r") as f:
            content = f.read()

        self.assertIn(".__main__.", content)


class TestClearOldLogs(ABCTestLogger):
    """Test the clear_old_logs function"""

    def test_call(self):
        """Test the function"""

        k_min = 2
        k_max = randint(1, 10)
        names = ["info", "debug", "warn", "errors"]

        for name in names:
            for k in range(k_max):
                filename = self.log_folder / f"{name}.log.{k}"
                filename.touch()

        clear_old_logs(self.log_folder, k_min=str(k_min))

        for name in names:
            for k in range(k_min + 1, k_max):
                filename = self.log_folder / f"{name}.log.{k}"

                self.assertFalse(filename.exists(), f"{filename} exists")

        clear_old_logs(log_path=None, k_min=k_min)
        clear_old_logs(log_path="not_existing_path", k_min=k_min)


class TestMeasureTime(unittest.TestCase):
    """Test the measure_time function"""

    @classmethod
    def setUpClass(cls):
        """Set the test context"""

        cls.log_folder = Path("logs/").absolute()
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)

        cls.log_folder.mkdir(exist_ok=True)

    def test_good_function(self):
        """Test a good function"""

        t = 5
        logger = create_logger(log_path=self.log_folder, name="good_logger")

        @measure_time(logger=logger)
        def _mock_good_func(t: int = 3):
            time.sleep(t)
            return 1

        _mock_good_func(t=t)

        with open(self.log_folder / "info.log", "r") as f:
            content = f.read()

        self.assertIn("_mock_good_func", content)

        regex = rf"[{t}|{t+1}]\.\d+\s\[s\]"
        matcher = re.compile(regex)
        objects = matcher.findall(content)
        self.assertGreater(len(objects), 0)

    def test_bad_function(self):
        """Test a good function"""

        t = 5
        logger = create_logger(log_path=self.log_folder, name="bad_logger")

        @measure_time(logger=logger)
        def _mock_bad_func(t: int = 5):
            return 1 / 0

        with self.assertRaises(ZeroDivisionError):
            _mock_bad_func(t=t)

        with open(self.log_folder / "errors.log", "r") as f:
            content = f.read()

        self.assertIn("_mock_bad_func", content)

    @classmethod
    def tearDownClass(cls):
        """Clean the test context"""

        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)


class TestDisplayArguments(unittest.TestCase):
    """Test the display_arguments function"""

    @classmethod
    def setUpClass(cls):
        """Set the test context"""

        cls.log_folder = Path("logs/").absolute()
        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)

        cls.log_folder.mkdir(exist_ok=True)

    def test_call(self):
        """Test a good function"""

        t = 5
        logger = create_logger(log_path=self.log_folder, name="my-logger")

        @display_arguments(logger=logger)
        def _mock_func(x, t: int = 3):
            time.sleep(t)
            return 1

        _mock_func(x=0, t=t)

        with open(self.log_folder / "info.log", "r") as f:
            content = f.read()

        self.assertIn("_mock_func(x=0, t=5)", content)

    @classmethod
    def tearDownClass(cls):
        """Clean the test context"""

        if cls.log_folder.exists():
            shutil.rmtree(cls.log_folder)


def build_suite():
    """Build the TestSuite"""
    suite = unittest.TestSuite()

    suite.addTest(TestRetrieveName("test_str"))
    suite.addTest(TestRetrieveName("test_list"))

    suite.addTest(TestCheckPath("test_str"))
    suite.addTest(TestCheckPath("test_path"))
    suite.addTest(TestCheckPath("test_float"))

    suite.addTest(TestConfigureLogger("test_configure_default"))
    suite.addTest(TestConfigureLogger("test_configure_none"))

    suite.addTest(TestCreateLogger("test_create_simple_logger"))
    suite.addTest(TestCreateLogger("test_create_logger_none_path"))
    suite.addTest(TestCreateLogger("test_create_named_logger"))
    suite.addTest(TestCreateLogger("test_create_with_none_yaml"))
    suite.addTest(TestCreateLogger("test_create_with_custom_yaml"))
    suite.addTest(TestCreateLogger("test_create_db"))
    suite.addTest(TestCreateLogger("test_from_main"))

    suite.addTest(TestClearOldLogs("test_call"))

    suite.addTest(TestMeasureTime("test_good_function"))
    suite.addTest(TestMeasureTime("test_bad_function"))

    suite.addTest(TestDisplayArguments("test_call"))

    return suite


if __name__ == "__main__":
    """The main script"""

    runner = unittest.TextTestRunner(failfast=True, output=xml_test_folder)
    runner.run(build_suite())
