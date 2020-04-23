
Installation
============

You can either use use :code:`pip` or you can install it from source using :code:`setuptools`.

Using pip
---------

The package releases are available on `Pypi <https://pypi.org/>`_. To install the package:

::

    pip install pywaterinfo


Using setuptools
----------------

After downloading the code from the repository, e.g. using `git`:

::

    git clone https://github.com/fluves/pywaterinfo

Go into the directory of the package itself and install the package using setuptools:

::

    cd pywaterinfo
    python setup.py install


Issues with SSL
---------------

Note that for some companies/environments, you may have to add a custom SSL certificate to the certifi repository for
the urllib queries to work. This is typically the case if you experience :code:`SSL: CERTIFICATE_VERIFY_FAILED` errors. There
in the utils module, there is a convenient helper routine to do just that: :func:`~pywaterinfo.utils.add_ssl_cert`.
Please contact your network administrator / ICT staff to obtain the relevant certificat to use inside your
domain to enable the https requests with urllib.
