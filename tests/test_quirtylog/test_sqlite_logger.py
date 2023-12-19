"""
---------------------
test_sqlite_logger.py
---------------------

This test check the sqlite module

To run the code
$ python test_sqlite_logger.py
"""
import logging
import sqlite3
import unittest

from pathlib import Path

import xmlrunner

from test_quirtylog.config import xml_test_folder

from quirtylog.sqlite_logger import SQLiteHandler


class TestSQLiteHandler(unittest.TestCase):
    """The base class for SQLiteHandler test"""

    @classmethod
    def setUpClass(cls):
        """Configure the test"""
        cls.db = Path('..') / 'logs'
        cls.db.mkdir(exist_ok=True)
        cls.db = cls.db / 'test.db'
        if cls.db.exists():
            cls.db.unlink()

    def test_sqlite_info(self):
        """Test the SQLLiteHandler"""

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        with self.assertRaises(TypeError):
            _ = SQLiteHandler(db=0)

        # sqlite handler
        sh = SQLiteHandler(db=self.db)
        sh.setLevel(logging.INFO)
        logging.getLogger().addHandler(sh)

        # test
        message = 'My awesome message'
        logging.info(message)

        self.assertTrue(self.db.exists())

        conn = sqlite3.connect(self.db)

        cursor = conn.execute(f'SELECT COUNT(*) FROM {sh.log_table};')
        rows = cursor.fetchall()[0][0]
        self.assertEqual(rows, 1)

        cursor = conn.execute(f'SELECT Message FROM {sh.log_table};')
        mess = cursor.fetchall()[0][0]
        self.assertEqual(message, mess)

        if self.db.exists():
            self.db.unlink()

    def test_sqlite_error(self):
        """Test the SQLLiteHandler"""

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        with self.assertRaises(TypeError):
            _ = SQLiteHandler(db=0)

        # sqlite handler
        sh = SQLiteHandler(db=str(self.db))
        sh.setLevel(logging.INFO)
        logging.getLogger().addHandler(sh)

        # test
        message = 'My awesome error'
        logging.error(message)

        self.assertTrue(self.db.exists())

        conn = sqlite3.connect(self.db)

        cursor = conn.execute(f'SELECT COUNT(*) FROM {sh.log_table};')
        rows = cursor.fetchall()[0][0]
        self.assertEqual(rows, 2)

        cursor = conn.execute(f'SELECT Message FROM {sh.log_table};')
        mess = cursor.fetchall()[0][0]
        self.assertEqual(message, mess)

        if self.db.exists():
            self.db.unlink()

    @classmethod
    def tearDownClass(cls):
        """Execute the tear down procedure"""
        if cls.db.exists():
            cls.db.unlink()


def build_suite():
    """Built the TestSuite"""
    suite = unittest.TestSuite()
    suite.addTest(TestSQLiteHandler('test_sqlite_info'))
    suite.addTest(TestSQLiteHandler('test_sqlite_error'))

    return suite


if __name__ == '__main__':
    """The main script"""

    runner = xmlrunner.XMLTestRunner(output=xml_test_folder)
    runner.run(build_suite())
