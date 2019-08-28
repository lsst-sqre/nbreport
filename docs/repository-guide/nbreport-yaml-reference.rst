.. _yaml-reference:

###################################
nbreport.yaml file format reference
###################################

Every report template repository has an :file:`nbreport.yaml` file that defines metadata about the report repository.
This page describes every field you might find in an :file:`nbreport.yaml` file, keeping in mind that some fields are optional.

An example :file:`nbreport.yaml` file:

.. code-block:: yaml

   handle: TESTR-001
   title: Characterization Metric Report Demo
   git_repo: https://github.com/lsst-sqre/nbreport
   ipynb: TESTR-001.ipynb
   assets:
     - '**/*.fits'
     - 'mydata.csv'
   git_repo_subdir: tests/TESTR-001
   ltd_product: testr-001
   published_url: https://testr-001.lsst.io
   ltd_url: https://keeper.lsst.codes/products/testr-001

handle
======

The handle is a short identifier for the report series.
nbreport does not prescribe a format for handles, but typically there is a series prefix and a serial number suffix:

.. code-block:: yaml

   handle: TESTR-001

.. _yaml-title:

title
=====

The title of the report series:

.. code-block:: yaml

   title: Characterization Metric Report Demo

.. _yaml-ipynb:

ipynb
=====

Set this field to the name of the report's Jupyter Notebook file, including the ``.ipynb`` extension:

.. code-block:: yaml

   ipynb: TESTR-001.ipynb

.. _yaml-assets:

assets (optional)
=================

If the report's Jupyter Notebook relies on other files to execute, and those files are part of the notebook template repository, you can mark them as *assets* with the ``assets`` field.
Assets are files, other than the ``ipynb`` notebook file, that are copied from the report repository into the report instance when it is rendered and computed (see `nbreport init`_).
Unlike the notebook (``ipynb`` file), **assets are not templated** — they are copied as-is.
Directory structure is preserved when asset files are copied from the report repository to the instance.

The assets field takes a **list** of strings.
Each string is a rule for matching asset file paths:

.. code-block:: yaml

   assets:
     - '**/*.fits'
     - 'mydata.csv'

There are three types of rules that designate assets:

- **The file name.**

  Simply name the file (relative to the root of the report repository) and it will be designated as an asset:

  .. code-block:: yaml

     assets:
       - 'mydata.csv'
       - 'images/image.fits`

  This example names two files, :file:`mydata.csv` and :file:`images/images.fits`, as assets.

- **A directory name.**

  The directory, and any files and subdirectories contained inside it, are copied from the report repository to the instance:

  .. code-block:: yaml

     assets:
       - 'images'

  In this example, the entire :file:`images` directory is designated as an asset.

- **A glob pattern.**

  In addition to simple globs (such as ``*.fits``), recursive globs are also supported (``**/*.fits``):

  .. code-block:: yaml

     assets:
       - 'images/*.fits'
       - '**/*.csv'

  In this example, any FITS file in the :file:`images` directory is designated as an asset.
  The second rule designates all CSV files as assets, regardless of what subdirectory contains them.

.. seealso::

   :doc:`how-to-use-python-modules`

.. _yaml-git-repo:

git\_repo (optional)
====================

The URL of the Git repository that this report template is published to.
This field is not necessary for local demos, though it is expected by the `nbreport register`_ command.
Setting this field also helps nbreport include information about the source Git repository in published report instances:

.. code-block:: yaml

   git_repo: https://github.com/lsst-sqre/nbreport

.. _yaml-git-repo-subdir:

git\_repo\_subdir (optional)
============================

If the report template is part of a Git repository (:ref:`git\_repo <yaml-git-repo>` is set), but the repository *is not* located at the root of that Git repository, you can specify the subdirectory where the report template is located by setting the ``git_repo_subdir`` field:

.. code-block:: yaml

   git_repo_subdir: tests/TESTR-001

In this example, the report repository is located in the ``tests/TESTR-001`` directory of the ``https://github.com/lsst-sqre/nbreport`` Git repository:

If the report template occupies the root of the Git repository, this field should be omitted:

.. _yaml-ltd-product:

ltd\_product (optional)
=======================

This is the name of the report's registered `product name`__ in the *LSST the Docs* RESTful HTTP API (see also :ref:`ltd\_url <yaml-ltd-url>`):

.. code-block:: yaml

   published_url: https://testr-001.lsst.io

.. __: https://ltd-keeper.lsst.io/products.html

Normally this field is automatically added when you run the `nbreport register`_ command to register the report with the nbreport server.
If the report is not formally published, this field should not be set.

.. _yaml-published-url:

published\_url (optional)
=========================

The ``published_url`` field is the URL for the homepage of a published report.
The homepage indexes all available instances of a report series:

.. code-block:: yaml

   published_url: https://testr-001.lsst.io

Normally this field is automatically added when you run the `nbreport register`_ command to register the report with the nbreport server.
If the report is not formally published, this field should not be set.

.. _yaml-ltd-url:

ltd\_url (optional)
===================

The ``ltd_url`` field is the URL for the report in the *LSST the Docs* RESTful HTTP API.
*LSST the Docs* is the service that hosts LSST documentation, including notebook-based reports:

.. code-block:: yaml

   ltd_url: https://keeper.lsst.codes/products/testr-001

Normally this field is automatically added when you run the `nbreport register`_ command to register the report with the nbreport server.
If the report is not formally published, this field should not be set.

.. seealso::

   The `LTD Keeper documentation`__ describes this API.

.. __: https://ltd-keeper.lsst.io/products.html#get--products-(slug)

.. _nbreport register: ../cli-reference.html#nbreport-register
.. _nbreport init: ../cli-reference.html#nbreport-init
