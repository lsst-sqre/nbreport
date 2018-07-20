"""Tests for the nbreport.instance module.
"""

from pathlib import Path

import pytest

from nbreport.instance import ReportInstance
from nbreport.repo import ReportRepo


def test_report_repo(tmpdir):
    """Test ReportRepo on the ``/tests/TESTR-000`` path.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'
    repo = ReportRepo(repo_path)

    instance_dirname = Path(str(tmpdir)) / 'TESTR-000-1'

    instance = ReportInstance.from_report_repo(repo, instance_dirname)

    assert instance.dirname == instance_dirname
    assert instance.dirname.exists()

    # Test re-opening the report instance, but with a string path
    instance2 = ReportInstance(str(instance_dirname))
    assert instance2.dirname == instance_dirname


def test_report_repo_overwrite(tmpdir):
    """Test modes for overwriting an existing instance directory.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'
    repo = ReportRepo(repo_path)
    instance_dirname = Path(str(tmpdir)) / 'TESTR-000-1'
    instance = ReportInstance.from_report_repo(repo, instance_dirname)
    assert instance.dirname == instance_dirname

    # Make another without overwrite=True
    with pytest.raises(OSError):
        ReportInstance.from_report_repo(repo, instance_dirname)

    # Make another with overwrite=true
    instance2 = ReportInstance.from_report_repo(repo, instance_dirname,
                                                overwrite=True)
    assert instance2.dirname == instance_dirname


def test_instance_not_found():
    """Test creating a ReportInstance when it does not exist.
    """
    with pytest.raises(OSError):
        ReportInstance('nonexistent')