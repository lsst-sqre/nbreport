"""Read and write user configuration (for storing GitHub personal access
tokens).
"""

__all__ = ('create_empty_config', 'read_config', 'get_config_path',
           'write_config', 'insert_github_config')

from pathlib import Path

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap


def create_empty_config():
    """Create an empty configuration object.

    Returns
    -------
    config : ``ruamel.yaml.comments.CommentedMap``
        The configuration data, as a native ``ruamel.yaml`` map type.
    """
    return CommentedMap({'github': None})


def read_config(path=None):
    """Read an existing nbreport YAML-formatted configuration file.

    Parameters
    ----------
    path : `str` or `pathlib.Path`, optional
        An optional, user-provided, override of the default configuration file
        path. The default path is ``~/.nbreport.yaml``.

    Returns
    ------
    config : ``ruamel.yaml.comments.CommentedMap``
        The configuration data, as a native ``ruamel.yaml`` map type.

    Raises
    ------
    FileNotFoundError
        Raised if the file does not exist.
    """
    yaml = ruamel.yaml.YAML()  # round-trip mode

    path = get_config_path(path=path)
    if not path.exists():
        raise FileNotFoundError(
            'Configuration file at {0!s} does not exist'.format(path))

    data = yaml.load(path)
    return data


def write_config(config, path=None):
    """Write the configuration data to a YAML file

    Parameters
    ----------
    config : ``ruamel.yaml.comments.CommentedMap``
        The configuration data, as a native ``ruamel.yaml`` map type.
    path : `str` or `pathlib.Path`, optional
        An optional, user-provided, override of the default configuration file
        path. The default path is ``~/.nbreport.yaml``.
    """
    yaml = ruamel.yaml.YAML()  # round-trip mode
    path = get_config_path(path=path)
    yaml.dump(config, path)


def get_config_path(path=None):
    """Get the path to the configuration file.

    By default, this file is ``~/.nbreport.yaml``.

    Parameters
    ----------
    path : `str` or `pathlib.Path`, optional
        An optional, user-provided, override of the default configuration file
        path.

    Returns
    -------
    path : `pathlib.Path`
        Path to the configuration file (whether it exists, or not).
    """
    if path is None:
        path = Path.home() / '.nbreport.yaml'
    else:
        path = Path(path)
    return path


def insert_github_config(config, username, token, token_note=None):
    """Insert a ``github`` field into the configuration data with GitHub
    authentication information (username and personal access token).

    Parameters
    ----------
    config : ``ruamel.yaml.comments.CommentedMap``
        The configuration data, as a native ``ruamel.yaml`` map type.
    username : `str`
        GitHub username.
    token : `str`
        GitHub personal access token belonging to the user.
    note : `str`, optional
        Note (YAML comment) to associate with the token field.

    Returns
    -------
    config : ``ruamel.yaml.comments.CommentedMap``
        The configuration data, as a native ``ruamel.yaml`` map type.
    """
    config['github'] = CommentedMap({
        'username': username,
        'token': token
    })
    if token_note is not None:
        config['github'].yaml_add_eol_comment(token_note, 'token')
    return config
