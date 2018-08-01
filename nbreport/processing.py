"""High-level functions that carry out work for the CLI subcommands.
"""

__all__ = ('is_url',)


from urllib.parse import urlparse


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
    if parts.scheme is not '':
        return True
    else:
        return False
