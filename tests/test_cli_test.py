"""Test the nbreport test CLI (nbreport.cli.test).
"""

from pathlib import Path

from click.testing import CliRunner
import nbformat

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


def test_config_option(tmpdir):
    """Test with config (-c) options to configure the template rendering.
    """
    runner = CliRunner()

    repo_path = Path(__file__).parent / 'TESTR-000'
    repo_path = repo_path.resolve()

    with runner.isolated_filesystem():
        args = [
            '--log-level', 'debug',
            'test',  # subcommand
            str(repo_path),  # first argument
            '-c', 'title', 'My sick report',
            '-c', 'a', '100',
            '-c', 'b', '200',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        print(result.output)

        assert result.exit_code == 0

        notebook_path = Path('TESTR-000-test') / 'TESTR-000.ipynb'
        nb = nbformat.read(str(notebook_path.resolve()),
                           as_version=nbformat.NO_CONVERT)

        assert nb.cells[0].source == (
            "# My sick report\n"
            "\n"
            "- By: Test Bot\n"
            "- Date: 2018-07-18"
        )

        assert nb.cells[1].outputs[0]['text'] == (
            'The answer is 300\n'
        )
