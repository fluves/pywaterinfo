
Installation
============

You can either use conda (either miniconda or anaconda) to install the package, use :code:`pip` or you can install it from source using :code:`setuptools`.

Using conda
-----------

TODO

You can setup a new environment in conda to install the package, or install the package in a current environment. In case you want to work in a new environment:

::

    conda create -n YOUR_ENV_NAME python=3.7

Either the existing environment or a new environment, first activate:

::

    conda activate YOUR_ENV_NAME

And install the pywaterinfo package:

::

    conda install pywaterinfo

Using pip
---------

TODO

Using setuptools
----------------

After downloading the code from the repository:

::

    git clone https://github.com/fluves/pywaterinfo

Go into the directory of the package itself and install the package using setuptools:

::

    cd pywaterinfo
    python setup.py install
