===========
pywaterinfo
===========

Python package to download time series data from `waterinfo.be <https://www.waterinfo.be/>`_.

Description
===========

pywaterinfo facilitates access to `waterinfo.be <https://www.waterinfo.be/>`_, a
website managed by the `Flanders Environment Agency (VMM) <https://en.vmm.be/>`_ and
`Flanders Hydraulics Research <https://www.waterbouwkundiglaboratorium.be>`_. The website
provides access to real-time water and weather related environmental variables for
Flanders (Belgium), such as rainfall, air pressure, discharge, and water level.
The package provides functions to search for stations and variables, and download
time series.

Installation
============

To install pywaterinfo with :code:`pip`:

::

    pip install pywaterinfo

Example
========

To initialize data requests from VMM, setup the :class:`~pywaterinfo.Waterinfo` class with `vmm` as input:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm")


The time series provided by waterinfo are all defined by a unique identifier called :code:`ts_id`. Each combination of a given **variable** (e.g. air pressure)
measured at a given **location** (e.g. Overpelt) with a certain **frequency** (e.g. 15min) is defined by an :code:`ts_id` identifier. Using such an identifier,
one can download the data of a given period with the command :func:`~pywaterinfo.Waterinfo.get_timeseries_values`. For example, the 15 min air pressure time series
at Overpelt has identifier :code:`ts_id = 78124042`. To get last day of data for the time series with ID :code:`78124042`:

::

    df = vmm.get_timeseries_values(78124042, period="P1D")

pywaterinfo returns the data as a `Pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/index.html>`_, which provides functionlities
to plot and manipulate the time series.

Requesting data from from HIC is very similar:

::

    from pywaterinfo import Waterinfo
    hic = Waterinfo("hic")

Get last day of data for the time series with ID :code:`39496010`, corresponding to high-resolution (5 min) conductivity measurements in Dendermonde:

::

    df = hic.get_timeseries_values(ts_id="39496010", period="P1D")

Next to the request of time series data for a given time series identifier, other
requests are supported as well. These functions provide multiple ways to search for the :code:`ts_id` you need to download
certain data. See the `documentation website <https://fluves.github.io/pywaterinfo/>`_ for more info.


Note on restrictions of the downloads
=====================================

The amount of data downloaded from `waterinfo.be <https://www.waterinfo.be/>`_ is limited via a credit system. You do not need to get a token right away to download data. For limited or irregular downloads, a token will not be required.

When you require more extended data requests, please request a download token from the `waterinfo.be <https://www.waterinfo.be/>`_ site administrators
via the e-mail address <hydrometrie@waterinfo.be> with a statement of which data and how frequently you would like to download data.
You will then receive a client-credit code that can be used to obtain a token that is valid for 24 hours, after which the token can be
refreshed with the same client-credit code. The handling of this token is done by the package itself, but it is important to use
the code when initializing the :class:`~pywaterinfo.Waterinfo` instance. For example, using a VMM token:

::

    from pywaterinfo import Waterinfo
    vmm_token = "YOUR TOKEN CODE"
    vmm = Waterinfo("vmm",  token=vmm_token)

Start to contribute
===================

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

In order to run all the tests, you need a HIC token, defined as an environmental variable ``HIC_TOKEN``. When you do
not have a HIC token, you can ignore the token tests for HIC webservice, be defining to not run the tests
marked with the `nohictoken` label:

::

    python setup.py test --addopts "-m 'not nohictoken'"

or with pytest directly:

::

    pytest -m 'not nohictoken'

The Github actions CI does have the token stored as a *secret*, so you do not really need a token for local testing, as eventual failures
will be noticed by the CI.

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

Acknowledgements
================

The package development and maintenance is supported by `Fluves <https://fluves.com/>`_. Part of the initial development of this package has been supported by `VITO <https://vito.be>`_.

|logo1|  |logo2|

.. |logo1| image:: _static/img/logo_fluves.png
    :width: 20%

.. |logo2| image:: _static/img/logo_vito.png
    :width: 20%

This package is just a small wrapper around waterinfo.be to facilitate researchers and other stakeholders in
downloading the data from `waterinfo.be <https://www.waterinfo.be/>`_. The availability of this data is made
possible by *de Vlaamse Milieumaatschappij, Waterbouwkundig Laboratorium, Maritieme Dienstverlening & Kust, Waterwegen
en Zeekanaal NV en De Scheepvaart NV*.

Other clients
=============

Besides this Python client to gather data from `waterinfo.be <https://www.waterinfo.be/>`_, there is also an R client available, the `wateRinfo <https://docs.ropensci.org/wateRinfo//>`_ package which is part of the `ropensci <https://ropensci.org/>`_ package suite and contains similar functionalities.

The `Flanders Hydraulics Research center <https://www.waterbouwkundiglaboratorium.be/en/>`_ also distributes clients for R, Python and Matlab upon request to download the data they share on `waterinfo.be <https://www.waterinfo.be/>`_. For more information, contact them directly via hic@vlaanderen.be.

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
