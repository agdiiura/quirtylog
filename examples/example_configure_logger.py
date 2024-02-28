"""
---------------------------
example_configure_logger.py
---------------------------

A script demonstrating the configuration of a logger using the 'quirtylog' module.

.. note::
    Ensure that 'quirtylog' is installed before running this script.
"""

import logging

from shutil import rmtree
from pathlib import Path

from quirtylog import configure_logger

logger = logging.getLogger(name="test-logger")


def main():
    """Execute the main function"""

    log_path = Path("logs/")

    logger.info("Invisible...")  # no-show
    configure_logger(log_path=log_path, config_file="default")
    logger.info("Let there be light...")

    rmtree(log_path)


if __name__ == "__main__":
    main()
