"""
-------------------------
test_exception_wrapper.py
-------------------------

This script demonstrates the usage of the exception wrapper defined in the 'quirtylog' module.
The wrapper captures and logs exceptions that occur during the execution of specified functions.
It uses the 'quirtylog' module to create a logger and applies the exception wrapper
to functions with different log levels.

Functions:
- good_function(): Executes a function with an INFO status and logs any exceptions.
- debug_function(): Executes a function with a DEBUG status and logs any exceptions.
- warning_function(): Executes a function with a WARNING status and logs any exceptions.
- bad_function(): Executes a function with an ERROR status and logs any exceptions.

Usage:
Run the main() function to execute all the example functions and observe the logged exceptions in
the specified log file.

.. note::
    Ensure that the 'quirtylog' module is installed before running this script.
"""
import time

from pathlib import Path

import quirtylog

log_path = Path().absolute() / 'logs'

logger = quirtylog.create_logger(log_path=log_path)


@quirtylog.measure_time(logger)
def good_function():
    """Execute a function that has an INFO status"""
    time.sleep(5)
    return 'abc'


@quirtylog.measure_time(logger, level='debug')
def debug_function():
    """Execute a function that has a DEBUG status"""
    time.sleep(5)
    return 0


@quirtylog.measure_time(logger, level='warning')
def warning_function():
    """Execute a function that has a WARNING status"""
    time.sleep(5)
    return 'efg'


@quirtylog.measure_time(logger)
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
