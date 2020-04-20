===========
pywaterinfo
===========

Python package to download time series data from waterinfo.be

Description
===========

pywaterinfo facilitates access to `waterinfo.be <https://www.waterinfo.be/>`_, a
website managed by the `Flanders Environment Agency (VMM) <https://en.vmm.be/>`_ and
`Flanders Hydraulics Research <https://www.waterbouwkundiglaboratorium.be>`_. The website
provides access to real-time water and weather related environmental variables for
Flanders (Belgium), such as rainfall, air pressure, discharge, and water level.
The package provides functions to search for stations and variables, and download
time series.

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

The resulting html files will be in the `docs\_build\html folder`. Double click the `index.html` to see the website on your local computer.

To keep the code formatting uniform, `black <https://black.readthedocs.io/en/stable/index.html>`_. is used to make the
code styling as consistent as possible. The required dependencies are part of the develop requirements in the `setup.cfg` file,
but make sure to install the pre-commit hook:

::

    pre-commit install
    pre-commit autoupdate

The Github actions CI job runs the unit tests, doctest, pre-commit checks and documentation building as well.


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
