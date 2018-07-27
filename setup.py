import os
from io import open

from setuptools import setup, find_packages


packagename = 'nbreport'
description = "LSST's notebook-based report system."
author = 'Association of Universities for Research in Astronomy'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/nbreport'
classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
]
keywords = 'lsst'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename, mode='r', encoding='utf-8').read()


long_description = read('README.rst')

# Core dependencies
install_requires = [
    'click>=6.7,<7.0',
    'cookiecutter>=1.6.0,<2.0.0',
    'nbformat',
    'nbconvert',
    'jupyter',  # needed by nbconvert
    'ruamel.yaml>=0.15.0,<0.16.0',
    'GitPython',
    'requests>=2.0',
]

# Setup dependencies
setup_requires = [
    'pytest-runner>=2.11.1,<3',
    'setuptools_scm'
]

# Test dependencies
tests_require = [
    'pytest==3.5.0',
    'pytest-cov==2.5.1',
    'pytest-flake8==1.0.0',
    'responses==0.9.0',
]

# Optional/development dependencies
docs_require = [
    'documenteer[pipelines]==0.3.0a5',
    'sphinx-click>=1.2.0,<1.3.0',
]
extras_require = {
    'dev': docs_require + tests_require
}


setup(
    name=packagename,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    keywords=keywords,
    packages=find_packages(exclude=['docs', 'tests*', 'data']),
    install_requires=install_requires,
    extras_require=extras_require,
    setup_requires=setup_requires,
    tests_require=tests_require,
    use_scm_version=True,
    # package_data={},
    entry_points={
        'console_scripts': [
            'nbreport = nbreport.cli.main:main',
        ]
    }
)
