"""
-----------------
test_singleton.py
-----------------

This test check the singleton module

To run the code
$ python test_singleton.py
"""
import xmlrunner
import unittest
from quirtylog.singleton import singleton
from config import xml_test_folder



@singleton
class Duck(object):
    """A test class"""

    @staticmethod
    def duck():
        """Execute the duck method"""
        print('Quack!')


class TestSingleton(unittest.TestCase):
    """The base class for singleton test"""

    def test_method(self):
        """Test the tqdm logger"""
        donald = Duck()
        duck = Duck()

        self.assertIs(donald, duck)


def build_suite():
    """Build the TestSuite"""
    suite = unittest.TestSuite()
    suite.addTest(TestSingleton('test_method'))

    return suite


if __name__ == '__main__':
    """The main script"""

    runner = xmlrunner.XMLTestRunner(output=xml_test_folder)
    runner.run(build_suite())
