"""Main command for rebreport CLI.
"""

__all__ = ('main',)

import logging
from pathlib import Path

import click

from ..userconfig import read_config, get_config_path, create_empty_config
from .compute import compute
from .login import login
from .register import register
from .init import init
from .issue import issue
from .test import test
from .upload import upload
from .render import render


# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--log-level', 'log_level',
    type=click.Choice(['warning', 'info', 'debug']),
    default='info',
    help='Logging level (for first-party messages). Default: ``info``.'
)
@click.option(
    '--config-file', 'config_path',
    type=click.Path(dir_okay=False, resolve_path=True),
    default=get_config_path,
    help='Path to the nbreport user configuration file. '
         'Default: ``~/.nbreport.yaml``.'
)
@click.option(
    '--server', default='https://api.lsst.codes',
    help='URL of the API host server. Default: ``https://api.lsst.codes``.'
)
@click.version_option(message='%(version)s')
@click.pass_context
def main(ctx, log_level, config_path, server):
    """nbreport is a command-line client for LSST's notebook-based report
    system. Use nbreport to initialize, compute, and upload report instances.
    """
    ch = logging.StreamHandler()
    if log_level.lower() == 'debug':
        # Detailed formatter for debugging
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)8s %(name)s | %(message)s')
    else:
        # Simper formatter for regular loggering
        formatter = logging.Formatter('%(levelname)8s %(message)s')
    ch.setFormatter(formatter)

    logger = logging.getLogger('nbreport')
    logger.addHandler(ch)
    logger.setLevel(log_level.upper())

    config_path = Path(config_path)
    try:
        config = read_config(path=config_path)
    except FileNotFoundError:
        config = create_empty_config()

    # Subcommands should use the click.pass_obj decorator to get this
    # ctx.obj object as the first argument.
    ctx.obj = {
        'config_path': config_path,
        'config': config,
        'server': server
    }


@main.command()
@click.argument('topic', default=None, required=False, nargs=1)
@click.pass_context
def help(ctx, topic, **kw):
    """Show help for any command.
    """
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic is None:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(main.commands[topic].get_help(ctx))


# Add subcommands from other modules
main.add_command(login)
main.add_command(register)
main.add_command(init)
main.add_command(render)
main.add_command(compute)
main.add_command(upload)
main.add_command(issue)
main.add_command(test)
