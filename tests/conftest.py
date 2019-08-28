"""Pytest test fixtures.
"""

from pathlib import Path

from click.testing import CliRunner
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
    path = Path(__file__).parent / 'TESTR-000'
    return path.resolve()


@pytest.fixture()
def testr_001_path():
    """Path to the TESTR-001 report repository.
    """
    path = Path(__file__).parent / 'TESTR-001'
    return path.resolve()


@pytest.fixture()
def testr_002_path():
    """Path to the TESTR-002 report repository.
    """
    path = Path(__file__).parent / 'TESTR-002'
    return path.resolve()


@pytest.fixture()
def runner():
    """Click CliRunner for invoking a command in testing.
    """
    return CliRunner()


@pytest.fixture()
def fake_registration():
    """Creates a callable that adds fake registration metadata to a report
    repository. This is necessary for creating instances with server-assigned
    IDs.
    """
    def _fake_registration(
            repo, ltd_product='testr-000',
            published_url='https://testr-000.lsst.io',
            ltd_url='https://keeper.lsst.codes/products/testr-000'):
        repo.config['ltd_product'] = ltd_product
        repo.config['published_url'] = published_url
        repo.config['ltd_url'] = ltd_url

    return _fake_registration
