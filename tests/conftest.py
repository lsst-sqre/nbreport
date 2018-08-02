"""Pytest test fixtures.
"""

from pathlib import Path

import pytest


@pytest.fixture()
def write_user_config():
    """Creates a callable that writes a mock .nbreport.yaml file into the
    current working directory. Used as a pytest fixture.
    """
    def _write_user_config(path='.nbreport.yaml'):
        data = (
            'github:\n'
            '  username: testuser\n'
            '  token: mytoken  # note for token\n'
        )
        with open(path, 'w') as fp:
            fp.write(data)

    return _write_user_config


@pytest.fixture()
def testr_000_path():
    """Path to the TESTR-000 report repository.
    """
    return Path(__file__).parent / 'TESTR-000'
