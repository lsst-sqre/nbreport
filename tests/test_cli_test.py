"""Test the nbreport test CLI (nbreport.cli.test).
"""

import nbreport.cli.main
from nbreport.instance import ReportInstance


def test_basic(testr_000_path, runner):
    """Test with no arguments except repo path.
    """
    with runner.isolated_filesystem():
        args = [
            'test',  # subcommand
            str(testr_000_path),  # first argument
        ]
        result = runner.invoke(nbreport.cli.main.main, args)

        assert result.exit_code == 0


def test_basic_with_dirname_arg(testr_000_path, runner):
    """Test with --id and -d arguments.
    """
    with runner.isolated_filesystem():
        args = [
            'test',  # subcommand
            str(testr_000_path),  # first argument
            '--id', '1',
            '-d', 'TESTR-000-1',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)

        assert result.exit_code == 0


def test_config_option(testr_000_path, runner):
    """Test with config (-c) options to configure the template rendering.
    """
    with runner.isolated_filesystem():
        args = [
            '--log-level', 'debug',
            'test',  # subcommand
            str(testr_000_path),  # first argument
            '-c', 'a', '100',
            '-c', 'b', '200',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        print(result.output)

        assert result.exit_code == 0

        instance = ReportInstance('TESTR-000-test')
        nb = instance.open_notebook()

        assert nb.cells[0].source == (
            "**TESTR-000-test**\n\n"
            "# Test Report\n\n"
            "- By: Test Bot\n"
            "- Date: 2018-07-18"
        )

        assert nb.cells[1].outputs[0]['text'] == (
            'The answer is 300\n'
        )


def test_from_git_clone(runner):
    """Test creating an instance from a GitHub original repository.
    """
    with runner.isolated_filesystem():
        args = [
            '--log-level', 'debug',
            'test',  # subcommand
            'https://github.com/lsst-sqre/nbreport',
            '--git-ref', 'master',
            '--git-subdir', 'tests/TESTR-000',
            '-c', 'a', '100',
            '-c', 'b', '200',
        ]
        result = runner.invoke(nbreport.cli.main.main, args)
        print(result.output)

        assert result.exit_code == 0
