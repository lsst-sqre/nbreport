##########
Change log
##########

0.7.4 (2019-02-12)
==================

- The ``click`` dependency is now floating.
  The click API used by nbreport is fairly stable, and unpinning improves compatibility with other package's in the user's environment.

0.7.3 (2019-08-28)
==================

- New ``assets`` field in the ``nbreport.yaml`` configuration file lets a user specify files in the template repository that are meant to be copied into a report instance's directory.
  Assets can be data files or Python modules that are needed for the report notebook to run.
- Added reference documentation for the ``nbreport.yaml`` file and also added how-to pages related to assets.

`DM-20954 <https://jira.lsstcorp.org/browse/DM-20954>`__.

0.7.2 (2019-08-08)
==================

- Update test dependencies (pytest 5.0.1, pytest-cov 2.7.1, pytest-flake8 1.0.4, responses 0.10.6).
- Update documentation dependencies (documenteer 0.5, sphinx-click 2.2.0).
- Improve the "Try it out" experience.

0.7.1 (2018-08-14)
==================

- For ``nbreport login``, now the user's GitHub username and password can *only* be provided through prompts.
  Previously the password could be specified as a command-line option as well.

0.7.0 (2018-08-12)
==================

This release fixes issues related to the integration of this ``nbreport`` command line client with the ``api.lsst.codes/nbreport`` backend microservice.

*New features:*

- Added the ``nbreport render`` command that renders the templated notebook of an initialized notebook instance that wasn't initially rendered (because no template variables were specified).

- Improved user messages from commands.

*Fixes:*

- Fixed bugs in ``nbreport.compute``.

- ``nbreport register`` now sends authentication data.

- The instance URL (``published_instance_url``) and API URL (``ltd_edition_url``) are now obtained during instance initialization.
  This matches when that data is readily available from the ``api.lsst.codes/nbreport`` backend microservice.

- Replace ``context`` with ``cookiecutter`` in an instance's ``nbreport.yaml`` field.
  By only reporting data from the ``cookiecutter`` template context in ``nbreport.yaml``, we avoid duplicating information that's copied into the template context, like ``instance_id`` and ``handle``.

- More thoroughly cast config to JSON-serializable dict when inserting the ``nbreport.yaml`` instance metadata into the notebook's metadata.
  In ruamel.yaml 0.15.52 (2018-08-09), the CommentedMap type is no longer a subclass of OrderedDict.
  This meant that the configs were no longer JSON-serializable when directly inserted into notebook metadata.

`DM-15416 <https://jira.lsstcorp.org/browse/DM-15416>`__.

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
