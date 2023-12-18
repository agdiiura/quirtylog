"""
-------------------
test_name_logger.py
-------------------

Test the logger name defined with the current frame
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
