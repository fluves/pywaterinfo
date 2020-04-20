===========
pywaterinfo
===========

Python package to download time series data from waterinfo.be

Description
===========

TODO

Start to develop
================

It's good practice to create a separate development environment for your package development. Use your preferred
system (or maybe integrated in your IDE) to setup a Python environment and see those docs to setup an environment
(conda, pyenv, virtualenv,,...). Once created, you can install all the developer dependencies using pip:

::

    pip install -e .[develop]

You can do a local development install to start using the package. Activate your environment and run:

::

    python setup.py develop


Tests are defined with `pytest <https://docs.pytest.org>`_. Write tests and run them using the command:

::

    python setup.py test


Documentation lives in the `docs` directory and is setup using `Sphinx package <http://www.sphinx-doc.org/en/master/>`_.
You can edit the documentation using any text editor and then generate the HTML output by with the command:

::

    python setup.py build_sphinx

The resulting html files will be in the `docs\_build\html folder`. Double click the `index.html` to see the website locally.

To keep the code formatting uniform, `black <https://black.readthedocs.io/en/stable/index.html>`_. is used to make the
code styling as consistent as possible. The required dependencies are part of the develop requirements in the `setup.cfg` file,
but make sure to install the pre-commit hook:

::

    pre-commit install

The Github actions CI job run the unit tests and builds the documentation as well.


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
