"""
---------------------
test_import_module.py
---------------------

Test the logger name defined with the current frame
"""

from pathlib import Path

from my_module import my_awesome_function  # noqa: F401, I900

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
