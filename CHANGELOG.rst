##########
Change log
##########

0.6.0 (2018-08-08)
==================

- Several new commands were added that make the ``nbreport`` command line client fully functional:

  - ``nbreport register`` command registers a report repo with LSST the Docs so that instances can be published.

  - ``nbreport init`` command initializes a new report instance (by reserving a number with the API server and optionally rendering template variables).

  - ``nbreport compute`` command computes a report instance's notebook.

  - ``nbreport upload`` command uploads a report instance to the API server, which publishes it to LSST the Docs.

  - ``nbreport issue`` command performs the equivalent of ``init``, ``compute``, and ``upload`` in a single step.

- Key metadata from each instance ``nbreport.yaml`` file is not available as a Jinja template variable, namely: ``handle``, ``title``, ``git_repo``, ``git_repo_subdir``, ``instance_id``, ``instance_handle``.
  These variables aren't part of the ``cookiecutter`` namespace and can't be overridden on the command line.

- Metadata from ``nbreport.yaml``, as well as the final set of ``cookiecutter`` template variables, are included in the notebook files's metadata.
  This provides a record of how the notebook was constructed, and will be used on the server to both render the notebook page and to provide filtering of notebooks.

- Refactored code related to reading ``~/.nbreport.yaml`` out of the ``nbreport login`` command and into the ``nbreport.userconfig`` module.
  The main command reads this file and passes data like the authentication token to subcommands.

- Refactored ``create_instance()`` out of the ``nbreport test`` command and into ``nbreport.processing`` so that multiple subcommands (``init``, ``issue``) can consume it.

`DM-15253 <https://jira.lsstcorp.org/browse/DM-15253>`__.

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
