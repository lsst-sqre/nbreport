"""Tests for the nbreport.repo module.
"""

from pathlib import Path

import nbformat
import pytest

from nbreport.repo import ReportRepo, ReportConfig


def test_report_repo(testr_000_path):
    """Test ReportRepo on the ``/tests/TESTR-000`` path.
    """
    repo = ReportRepo(testr_000_path)

    assert repo.dirname == testr_000_path
    assert repo.context_path == testr_000_path / 'cookiecutter.json'
    assert repo.config_path == testr_000_path / 'nbreport.yaml'
    assert isinstance(repo.config, ReportConfig)
    assert isinstance(repo.open_notebook(), nbformat.NotebookNode)
    # This repo doesn't have assets
    assert len(repo.asset_paths) == 0


def test_report_repo_from_str(testr_000_path):
    """Test creating a ReportRepo on the ``/tests/TESTR-000`` path from a
    string.
    """
    repo = ReportRepo(str(testr_000_path))
    assert repo.dirname == testr_000_path


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


def test_report_config_read(testr_000_path):
    """Test reading the ReportConfig using ``/tests/TESTR-000/nbreport.yaml``.
    """
    repo = ReportRepo(testr_000_path)
    assert repo.config['handle'] == 'TESTR-000'
    assert repo.config['title'] == 'Test Report'
    assert repo.config['ipynb'] == 'TESTR-000.ipynb'

    assert repr(repo.config) \
        == "ReportConfig('{0!s}')".format(repo.config_path)

    assert str(repo.config) == (
        'handle: TESTR-000\n'
        'title: Test Report\n'
        'git_repo: https://github.com/lsst-sqre/nbreport\n'
        'git_repo_subdir: tests/TESTR-000\n'
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

    # Test __contains__
    assert 'title' in config
    assert 'not-here' not in config


def test_report_repo_asset_paths(testr_002_path):
    """Test getting asset paths from a repo with lots of them.
    """
    repo = ReportRepo(testr_002_path)
    asset_paths = repo.asset_paths

    assert repo.dirname / 'assetmodule.py' in asset_paths
    assert repo.dirname / '1.txt' in asset_paths
    assert repo.dirname / '2.txt' in asset_paths
    assert repo.dirname / 'a/3.txt' in asset_paths
    assert repo.dirname / 'a/b/4.txt' in asset_paths
    assert repo.dirname / 'md/1.md' in asset_paths
    assert repo.dirname / 'md/2.md' in asset_paths
