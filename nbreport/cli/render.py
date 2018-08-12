"""Implementation for the ``nbreport render`` command that renders a
templated notebook instance.
"""

__all__ = ('render',)

import click

from ..instance import ReportInstance


@click.command()
@click.argument(
    'instance_path', default=None, required=True, nargs=1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    '-c', '--config', 'template_variables', nargs=2, type=str, multiple=True,
    help='Template key-value pairs. For example, if the report has a template '
         'variable called ``cookiecutter.myvar``, you can provide it as '
         '``-c myvar "Hello World!"``. You can provide multiple '
         '-c/--config options.'
)
@click.pass_context
def render(ctx, instance_path, template_variables):
    """Render the notebook template of a newly-create instance.

    Use this command to render the notebook template if you didn't provide
    template variables with the ``nbreport init`` command.

    **Required arguments**

    ``INSTANCE_PATH``
        The path to the report repository directory. You can create an
        instance with the ``nbreport init`` command.
    """
    template_variables = dict(template_variables)
    if len(template_variables) == 0:
        # Set an empty dictionary to designate that we *are* rendering the
        # template variables, but we're entirely using defaults from the
        # cookiecutter.json file.
        template_variables = {}

    instance = ReportInstance(instance_path)
    instance.render(context=template_variables)

    click.echo('Rendered {0!s}'.format(instance.ipynb_path))
