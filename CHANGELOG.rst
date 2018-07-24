##########
Change log
##########

0.3.0 (2018-07-23)
==================

- New ``nbreport`` command-line interface, implemented with Click.

- New ``nbreport test`` command that is designed for locally testing report repositories and ensuring that they render and compute correctly.
  This command creates a report instance, renders the templated variables, and computes the notebook.

- New ``nbreport.repo`` module to handle report repositories and their configurations.

- New ``nbreport.instance`` module to handle report instances.

- New ``nbreport.compute`` module to run notebook instances to compute their cell outputs.

`DM-15167 <https://jira.lsstcorp.org/browse/DM-15167>`__.

0.2.0 (2018-07-18)
==================

This version introduces the ``nbreport.templating`` module.
This module provides functions for building a Jinja context from a ``cookiecutter.json`` file and for rendering the ``source`` fields of notebook cells as Cookiecutter-compatible Jinja templates.

This release also adds API reference documentation to the nbreport.lsst.io site.

`DM-15150 <https://jira.lsstcorp.org/browse/DM-15150>`__.

0.1.0 (2018-07-17)
==================

Initial packaging of the nbreport project.
