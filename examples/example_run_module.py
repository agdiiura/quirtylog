"""
---------------------
example_run_module.py
---------------------

This script tests the execution of quirtylog as a module.
It demonstrates the creation of a logger and its use within a simple test function.

Usage:
Run the script to execute the 'main' function, which logs an informational message.

.. note::
    Ensure that the 'quirtylog' module is installed before running this script.
"""

import time
import logging

logger = logging.getLogger(__name__)


def main():
    """Execute the main function"""
    time.sleep(1)
    logger.info("Execute main function")
    time.sleep(1)


main()
logger.info("Done!")
if __name__ == "__main__":
    pass
