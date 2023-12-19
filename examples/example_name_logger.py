"""
----------------------
example_name_logger.py
-----------------------

This script tests the logger name definition using the 'quirtylog' module based on the current frame.
It demonstrates the creation of a logger and its use within a simple test function.

Usage:
Run the script to execute the 'func' function, which logs an informational message and returns a value.

.. note::
    Ensure that the 'quirtylog' module is installed before running this script.
"""

from pathlib import Path

import quirtylog

log_path = Path().absolute() / 'logs'

logger = quirtylog.create_logger(log_path=log_path)


def func():
    """Print on info and return a value using a simple test function"""
    logger.info('In func')
    return 0


if __name__ == '__main__':
    func()
