"""
------------
my_module.py
------------

A module for test about import from different modules
See documentation: https://docs.python.org/3/howto/logging.html#logging-from-multiple-modules
"""
import logging

logger = logging.getLogger(__name__)

__all__ = ['my_awesome_function']


def my_awesome_function():
    """Execute the test function"""
    logger.info('Here in my_module.py')


if __name__ == '__main__':
    pass
