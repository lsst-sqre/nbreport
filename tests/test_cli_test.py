"""Test the nbreport test CLI (nbreport.cli.test).
"""

from pathlib import Path

from click.testing import CliRunner

import nbreport.cli.main


def test_basic(tmpdir):
    """Test with no arguments except repo path.
    """
    runner = CliRunner()

    repo_path = Path(__file__).parent / 'TESTR-000'
    repo_path = repo_path.resolve()

    with runner.isolated_filesystem():
        args = [
            'test',  # subcommand
            str(repo_path),  # first argument
        ]
        result = runner.invoke(nbreport.cli.main.main, args)

        assert result.exit_code == 0


def test_basic_with_dirname_arg(tmpdir):
    """Test with --id and -d arguments.
    """
    runner = CliRunner()

    repo_path = Path(__file__).parent / 'TESTR-000'
    repo_path = repo_path.resolve()

    with runner.isolated_filesystem():
        args = [
            'test',  # subcommand
            str(repo_path),  # first argument
            '--id', '1',
            '-d', 'TESTR-000-1',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)

        assert result.exit_code == 0
