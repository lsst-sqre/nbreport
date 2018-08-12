"""Tests for the ``nbreport upload`` command.
"""

from pathlib import Path
import shutil

import responses

import nbreport.cli.main
from nbreport.repo import ReportRepo
from nbreport.compute import compute_notebook_file
from nbreport.processing import create_instance


@responses.activate
def test_upload(write_user_config, testr_000_path, runner, fake_registration):
    responses.add(
        responses.POST,
        'https://api.lsst.codes/nbreport/reports/testr-000/'
        'instances/test/notebook',
        json={
            'queue_url': 'https://example.com/queue/12345'
        },
        status=202)

    with runner.isolated_filesystem():
        # Copy the repo into this isolated workspace
        repo_path = Path.cwd() / 'TESTR-000'
        shutil.copytree(str(testr_000_path), str(repo_path))
        assert repo_path.exists()

        # Make a repo with faked registration
        repo = ReportRepo(repo_path)
        fake_registration(repo)

        # Create a mock .nbreport.yaml file with auth data
        write_user_config('.nbreport.yaml')

        instance = create_instance(
            repo,
            instance_id='test',
            template_variables={},
            instance_path=Path('TESTR-000-test'))

        compute_notebook_file(instance.ipynb_path)

        args = [
            '--config-file', '.nbreport.yaml',
            'upload',
            str(instance.dirname)
        ]

        result = runner.invoke(nbreport.cli.main.main, args)
        print(result.output)
        assert result.exit_code == 0

        request = responses.calls[0].request
        assert request.url == (
            'https://api.lsst.codes/nbreport/reports/testr-000/'
            'instances/test/notebook')
        assert request.headers['Content-Type'] == 'application/x-ipynb+json'

        with open(instance.ipynb_path, 'rb') as fp:
            nbdata = fp.read()
            assert request.body == nbdata
