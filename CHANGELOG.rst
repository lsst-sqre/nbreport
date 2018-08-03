##########
Change log
##########

0.5.1 (2018-08-03)
==================

- Add ``read:org`` role to the personal access token obtained by ``nbreport login``.
  This role is necessary for the api.lsst.codes/nbreport service to _authorize_ a user based on their GitHub organization memberships.
  The list of token roles is now ``read:org`` and ``read:user``.

`DM-15199 <https://jira.lsstcorp.org/browse/DM-15199>`__.

0.5.0 (2018-07-27)
==================

- New ``nbreport login`` command that generates a GitHub personal access token on behalf of the user and caches it in a ``~/.nbreport.yaml`` file.
  LSST's notebook-based report system uses GitHub to authenticate users submitting reports and to authorize the publication based on GitHub organization memberships.

- New dependencies on ``requests`` and ``responses``.

`DM-15216 <https://jira.lsstcorp.org/browse/DM-15216>`__.

0.4.0 (2018-07-25)
==================

- ``nbreport test`` can now open a report repository from a remote Git repository (such as one on GitHub).

- New ``nbreport.ReportRepository.git_clone()`` class method to clone a report repository from GitHub.

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
