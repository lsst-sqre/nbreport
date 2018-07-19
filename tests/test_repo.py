"""Tests for the nbreport.repo module.
"""

from pathlib import Path

import pytest

from nbreport.repo import ReportRepo


def test_report_repo():
    """Test ReportRepo on the ``/tests/TESTR-000`` path.
    """
    repo_path = Path(__file__).parent / 'TESTR-000'

    repo = ReportRepo(repo_path)

    assert repo.dirname == repo_path


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
