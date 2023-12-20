"""
------------------------
example_import_module.py
------------------------

This script tests the integration of the 'quirtylog' module with a custom module ('my_module')
and demonstrates the creation of a logger with a specified database connection.

Usage:
Run the main() function to execute the script, which logs information before and after
calling 'my_awesome_function' from 'my_module'.

The script uses the 'quirtylog' module to create a logger with the specified log path and
database connection ('log.db').

.. note::
    Ensure that 'quirtylog' is installed before running this script.
"""

from pathlib import Path

from my_module import my_awesome_function

import quirtylog

log_path = Path().absolute() / 'logs'
logger = quirtylog.create_logger(log_path=log_path, db='log.db')


def main():
    """Execute the main function"""

    logger.info('Before')
    my_awesome_function()
    logger.info('After')


if __name__ == '__main__':
    main()
