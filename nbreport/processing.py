"""High-level functions that carry out work for the CLI subcommands.
"""

__all__ = ('is_url', 'create_instance')

import logging
import pathlib
from urllib.parse import urlparse, urljoin

import click
import requests

from .instance import ReportInstance


def is_url(path_or_url):
    """Test if the token represents a URL or a local path.

    Parameters
    ----------
    path_or_url : `str`
        Token string that can either be a URL or not.

    Returns
    -------
    is_url : `bool`
        Returns `True` is the token is in fact a URL. `False` otherwise.
    """
    parts = urlparse(path_or_url)
    if parts.scheme != '':
        return True
    else:
        return False


def create_instance(report_repo, instance_id=None, template_variables=None,
                    instance_path=None, overwrite=False,
                    github_username=None, github_token=None, server=None):
    """Create a report instance.

    Parameters
    ----------
    report_repo : `nbreport.repo.ReportRepo`
        Report repository.
    instance_id : `str`, optional
        The instance identifier. Leave as `None` to reserve a new instance
        with the server.
    template_variables : `dict`, optional
        If provided, these key-value pairs are used to render the templated
        notebook. If `None`, the templated notebook *is not* rendered. If
        an empty `dict`, the templated notebook is renderd but entirely with
        defaults defined in ``cookiecutter.json``.
    instance_path : `str` or `pathlib.Path`, optional
        If provided, this is the directory of the report instance. Otherwise,
        a directory will be automatically created in the current working
        directory, formatted as ``{{handle}}-{{id}}``.
    overwrite : `bool`, optional
        If `True`, and a directory of the same name as ``instance_path``
        exists, that directory is overwritten with the new instance.
    github_username : `str`, optional
        GitHub username. Only required if ``instance_id`` is None.
    github_token : `str`, optional
        Personal access token for the GitHub user. Only required if
        ``instance_id`` is None.
    server : `str`, optional
        Hostname of the api.lsst.codes, or equivalent, service. Only required
        if ``instance_id`` is None.

    Returns
    -------
    instance : `nbreport.instance.ReportInstance`
        A `~nbreport.instance.ReportInstance` corresponding to an instance
        directory on the local filesystem.
    """
    logger = logging.getLogger()

    if instance_id is None:
        # Register instance with server
        instance_data = _reserve_instance(report_repo, server, github_username,
                                          github_token)
        instance_id = instance_data.pop('instance_id')
    else:
        instance_data = {}

    if instance_path is None:
        instance_path = pathlib.Path(
            '{0}-{1}'.format(str(report_repo.dirname.name), instance_id))
    else:
        instance_path = pathlib.Path(instance_path)

    instance = ReportInstance.from_report_repo(
        report_repo, instance_path, instance_id, overwrite=overwrite,
        context=template_variables, **instance_data)
    logger.debug('Created instance %s at %s', instance, instance_path)

    return instance


def _reserve_instance(report_repo, server, github_username, github_token):
    """Reserve a new instance ID from api.lsst.codes/nbreport.

    This function is only intended to be used by `create_instance`.

    Parameters
    ----------
    report_repo : `nbreport.repo.ReportRepo`
        Report repository.
    server : `str`
        Hostname of the api.lsst.codes, or equivalent, service.
    github_username : `str`
        GitHub username.
    github_token : `str`
        Personal access token for the GitHub user.

    Returns
    -------
    instance_data : `dict`
        Instance data, with keys:

        - ``published_instance_url``
        - ``ltd_edition_url``
        - ``instance_id``
    """
    try:
        ltd_product = report_repo.config['ltd_product']
    except KeyError:
        raise click.UsageError(
            'Field "ltd_product" not found in the report repository\'s '
            'nbreport.yaml file. Try registering the report by running '
            '"nbreport register".')

    url = urljoin(server, '/nbreport/reports/{product}/instances/'.format(
        product=ltd_product))
    response = requests.post(url, auth=(github_username, github_token))
    response.raise_for_status()
    data = response.json()
    instance_data = {
        'published_instance_url': data['published_url'],
        'ltd_edition_url': data['ltd_edition_url'],
        'instance_id': data['instance_id']
    }
    return instance_data
