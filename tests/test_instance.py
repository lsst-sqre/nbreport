"""Tests for the nbreport.instance module.
"""

from pathlib import Path

import pytest
import nbformat

from nbreport.instance import ReportInstance
from nbreport.repo import ReportRepo


def test_report_repo(tmpdir, testr_000_path):
    """Test ReportRepo on the ``/tests/TESTR-000`` path.
    """
    repo = ReportRepo(testr_000_path)
    instance_dirname = Path(str(tmpdir)) / 'TESTR-000-1'

    instance = ReportInstance.from_report_repo(
        repo, instance_dirname, '1')

    assert instance.dirname == instance_dirname
    assert instance.dirname.exists()
    assert instance.config['handle'] == 'TESTR-000'
    assert instance.config['instance_id'] == '1'
    assert instance.config['instance_handle'] == 'TESTR-000-1'
    assert isinstance(instance.open_notebook(), nbformat.NotebookNode)

    # Test re-opening the report instance, but with a string path
    instance2 = ReportInstance(str(instance_dirname))
    assert instance2.dirname == instance_dirname


def test_report_repo_overwrite(tmpdir, testr_000_path):
    """Test modes for overwriting an existing instance directory.
    """
    repo = ReportRepo(testr_000_path)
    instance_dirname = Path(str(tmpdir)) / 'TESTR-000-1'
    instance = ReportInstance.from_report_repo(repo, instance_dirname, '1')
    assert instance.dirname == instance_dirname

    # Make another without overwrite=True
    with pytest.raises(OSError):
        ReportInstance.from_report_repo(repo, instance_dirname, '1')

    # Make another with overwrite=true
    instance2 = ReportInstance.from_report_repo(repo, instance_dirname, '1',
                                                overwrite=True)
    assert instance2.dirname == instance_dirname


def test_instance_not_found():
    """Test creating a ReportInstance when it does not exist.
    """
    with pytest.raises(OSError):
        ReportInstance('nonexistent')


def test_asset_copy(tmpdir, testr_002_path):
    """Test copying assets that come with the TESTR-002 demo repo.
    """
    repo = ReportRepo(testr_002_path)
    instance_dirname = Path(str(tmpdir)) / 'TESTR-002-1'

    ReportInstance.from_report_repo(
        repo, instance_dirname, '1')

    print(list(instance_dirname.glob('**/*')))
    assert (instance_dirname / 'assetmodule.py').exists()
    assert (instance_dirname / '1.txt').exists()
    assert (instance_dirname / '2.txt').exists()
    assert (instance_dirname / 'a/3.txt').exists()
    assert (instance_dirname / 'a/b/4.txt').exists()
    assert (instance_dirname / 'md/1.md').exists()
    assert (instance_dirname / 'md/2.md').exists()
