"""Main command for rebreport CLI.
"""

__all__ = ('main',)

import logging

import click

from .login import login
from .test import test


# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--log-level', 'log_level',
    type=click.Choice(['warning', 'info', 'debug']),
    default='info',
    help='Logging level (for first-party messages). Default: ``info``.'
)
@click.version_option(message='%(version)s')
@click.pass_context
def main(ctx, log_level):
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

    # Subcommands should use the click.pass_obj decorator to get this
    # ctx.obj object as the first argument.
    ctx.obj = {
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
main.add_command(test)
