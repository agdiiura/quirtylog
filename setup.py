#!/usr/bin/env python

from pathlib import Path

from setuptools import setup, find_packages


def read_readme(path: Path):
    """
    Read the README.md file and return it as a string

    :param path: (Path) package path
    :return readme: (str) the README file
    """

    file_name = path / 'README.md'
    with open(file_name, 'r') as file:
        readme = file.read()

    return readme


def _read_reqs(path: Path, filename: str) -> list:
    """Read requirements base function"""
    file_name = path / filename
    with open(file_name, 'r') as file:
        reqs = file.read().splitlines()

    return reqs


def read_reqs(path: Path) -> list:
    """
    Read the requirements.txt file

    :param path: (Path) package path
    :return requirements: (list) list of requirements
    """
    reqs = _read_reqs(path=path, filename='requirements.txt')
    reqs.append('setuptools-git-versioning')

    return reqs


def read_docreqs(path: Path) -> list:
    """
    Read the docs-requirements.txt file

    :param path: (Path) package path
    :return docs-requirements: (list) list of requirements
    """
    return _read_reqs(path=path, filename='docs-requirements.txt')


def read_buildreqs(path: Path) -> list:
    """
    Read the build-requirements.txt file

    :param path: (Path) package path
    :return build-requirements: (list) list of requirements
    """
    return _read_reqs(path=path, filename='build-requirements.txt')


def read_authors(path: Path) -> str:
    """
    Read the AUTHORS.rst file as a str

    :param path: (Path) input file
    :return: authors: (str) authors list
    """
    file_name = path / 'AUTHORS.rst'
    with open(file_name, 'r') as file:
        authors = file.read().replace('\n\n', ', ')

    return authors


if __name__ == '__main__':
    """The main script"""

    absolute_path = Path(__file__).resolve().parent

    pkg_name = 'quirtylog'
    requirements = read_reqs(absolute_path)

    packages = find_packages()

    # TODO package_dir is not compatible with develop mode, see https://github.com/pypa/setuptools/issues/230
    # TODO thus we exclude it in the setup function
    package_dir = {pkg_name: str(absolute_path / pkg_name)}

    setup_kwargs = dict(
        name=pkg_name,
        version_config={
            'dirty_template': '{tag}'
        },
        description='Quick & dirty logging package',
        long_description=read_readme(absolute_path),
        author=read_authors(absolute_path),
        author_email='andreadiiura@gmail.com',
        packages=packages,
        package_data={
            '': ['*.yaml']
        },
        # package_dir=package_dir,
        install_requires=requirements,
        setup_requires=requirements,
        classifiers=[
            'Programming Language :: Python :: 3.11',
        ],
        extra_requires={
            'docs': read_docreqs(absolute_path),
            'develop': read_buildreqs(absolute_path)
        }
    )

    setup(**setup_kwargs)
