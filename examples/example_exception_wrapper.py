"""
-------------------------
test_exception_wrapper.py
-------------------------

Test the wrapper exception defined in quirtylog
"""
import time

from pathlib import Path

import quirtylog

log_path = Path().absolute() / 'logs'

logger = quirtylog.create_logging(log_path=log_path)


@quirtylog.exception(logger)
def good_function():
    """Execute a function that has an INFO status"""
    time.sleep(5)
    return 'abc'


@quirtylog.exception(logger, level='debug')
def debug_function():
    """Execute a function that has a DEBUG status"""
    time.sleep(5)
    return 0


@quirtylog.exception(logger, level='warning')
def warning_function():
    """Execute a function that has an WARNING status"""
    time.sleep(5)
    return 'efg'


@quirtylog.exception(logger)
def bad_function():
    """Execute a function that has an ERROR status"""
    return 1 / 0.


def main():
    """Execute the main script"""

    good_function()
    debug_function()
    warning_function()
    bad_function()


if __name__ == '__main__':
    main()
