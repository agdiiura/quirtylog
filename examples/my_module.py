"""
------------
my_module.py
------------

This module serves as a test module for demonstrating imports from different modules and
logging functionalities.
It contains a function 'my_awesome_function' that logs information using the Python logging module.

For more details on the Python logging module, see: https://docs.python.org/3/library/logging.html
"""
import logging

logger = logging.getLogger(__name__)

__all__ = ['my_awesome_function']


def my_awesome_function():
    """Execute the test function"""
    logger.info('Here in my_module.py')


if __name__ == '__main__':
    pass
