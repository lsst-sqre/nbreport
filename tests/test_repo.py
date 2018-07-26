"""Tests for the nbreport.repo module.
"""

from pathlib import Path

import nbformat
import pytest

from nbreport.repo import ReportRepo, ReportConfig


def test_report_repo():
    """Test ReportRepo on the ``/tests/TESTR-000`` path.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'

    repo = ReportRepo(repo_path)

    assert repo.dirname == repo_path
    assert repo.context_path == repo_path / 'cookiecutter.json'
    assert repo.config_path == repo_path / 'nbreport.yaml'
    assert isinstance(repo.config, ReportConfig)
    assert isinstance(repo.open_notebook(), nbformat.NotebookNode)


def test_report_repo_from_str():
    """Test creating a ReportRepo on the ``/tests/TESTR-000`` path from a
    string.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'
    repo = ReportRepo(str(repo_path))
    assert repo.dirname == repo_path


def test_report_repo_not_found():
    """Test creating a ReportRepo on a non-existent directory.
    """
    repo_path = Path(__file__).parent / 'nonexistent'
    with pytest.raises(OSError):
        ReportRepo(str(repo_path))


def test_report_repo_git_clone(tmpdir):
    """Test creating a ReportRepo from a git clone.
    """
    repo = ReportRepo.git_clone(
        'https://github.com/lsst-sqre/nbreport',
        checkout='master',
        clone_base_dir=tmpdir,
        subdir='tests/TESTR-000')
    assert repo.dirname.is_dir()
    assert repo.ipynb_path.exists()


def test_report_config_read():
    """Test reading the ReportConfig using ``/tests/TESTR-000/nbreport.yaml``.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'
    repo = ReportRepo(repo_path)
    assert repo.config['handle'] == 'TESTR-000'
    assert repo.config['title'] == 'Test Report'
    assert repo.config['ipynb'] == 'TESTR-000.ipynb'

    assert repr(repo.config) \
        == "ReportConfig('{0!s}')".format(repo.config_path)

    assert str(repo.config) == (
        'handle: TESTR-000\n'
        'title: Test Report\n'
        'ipynb: TESTR-000.ipynb\n'
    )


def test_report_config_write(tmpdir):
    """Test creating a ReportConfig from scratch and writing it.
    """
    path = Path(tmpdir) / 'nbreport.yaml'
    config = ReportConfig(path)

    assert len(config.keys()) == 0

    with pytest.raises(KeyError):
        config['handle']

    data = {
        'handle': 'TESTR-000',
        'title': 'Test Report',
        'ipynb': 'TESTR-000.ipynb'
    }

    # Test update and __getitem__
    config.update(data)
    assert config['handle'] == data['handle']
    assert config['title'] == data['title']
    assert config['ipynb'] == data['ipynb']

    # Test items
    data_rebuilt = {k: v for k, v in config.items()}
    assert data == data_rebuilt

    # Test __setitem__
    config['title'] = 'Revised Test Report'
    assert config['title'] == 'Revised Test Report'
