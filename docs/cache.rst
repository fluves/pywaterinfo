

Caching
=======

To overcome redundant requests of the same data to the waterinfo endpoints, the package relies on the `requests-cache <https://pypi.org/project/requests-cache/>`_ package to cache the :code:`GET` requests.

The cache is stored in a sqlite database called :code:`pywaterinfo_cache.sqlite` and the default retention time of the cache is 7 days.
When you want to make sure to not use a cached requests, make sure to empty the cache first using the :func:`~pywaterinfo.Waterinfo.clear_cache` method:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm")
    vmm.clear_cache()
    vmm.get_timeseries_list(station_no="ME09_012")


To see if the response is retrieved from cache or not, activate the loggin, see `page on logging <logging>`_.
