"""
---------
config.py
---------

The configuration file for test_quirtylog
"""

from pathlib import Path

__all__ = ["xml_test_folder"]

config_path = Path(__file__).absolute().parent


def get_xml_test_folder(verbose: bool = True) -> str:
    """Serve a test-reports folder based on the current system environment"""
    path = config_path.parent / "test-reports"
    path.mkdir(exist_ok=True)

    if verbose:
        print(f"xml-test-folder: {path}")

    return str(path)


xml_test_folder = get_xml_test_folder()

if __name__ == "__main__":
    """The main script"""

    pass
