
.. _cache:

Caching
=======

To overcome redundant requests of the same data to the waterinfo endpoints, the package relies on the `requests-cache <https://pypi.org/project/requests-cache/>`_ package to cache the :code:`GET` requests. The
cache feature is opt-in (not installed/activated by default), but can be used after installing the cache dependency packages:

::

    pip install pywaterinfo[cache]

To use the cache, activate it on the initialization of the ``Waterinfo`` class:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm", cache=True)

The cache is stored in a sqlite database called :code:`pywaterinfo_cache.sqlite` and the default retention time of the cache is 7 days.
When you want to make sure to not use a cached requests, make sure to empty the cache first using the :func:`~pywaterinfo.Waterinfo.clear_cache` method:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm")
    vmm.clear_cache()
    vmm.get_timeseries_list(station_no="ME09_012")


To see if the response is retrieved from cache or not, activate the loggin, see `page on logging <logging>`_.

.. warning::

    When downloading a lot of (small) data with many requests in a short amount of time the cache can grow quickly. This increases the computational time to check if a request already has been made and can be retrieved from the cache. Clearing the cache can overcome increasing initializaton time:

    ::

        from pywaterinfo import Waterinfo
        vmm = Waterinfo("vmm")
        vmm.clear_cache()

    When the initialization time (Creating the ``Waterinfo`` class) goes up to more than a minute without a network timeout error, clearing the cache is worthwhile to test.
