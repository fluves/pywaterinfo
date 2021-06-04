.. _waterinfo:

========
Tutorial
========

The Waterinfo module facilitates access to `waterinfo.be <https://waterinfo.be>`_, a website managed by the Flanders
Environment Agency (VMM) and Flanders Hydraulics Research (HIC). The website provides access to real-time water
and weather related environmental variables for Flanders (Belgium), such as rainfall, air pressure,
discharge, and water level. The package provides functions to search for stations and variables,
and download time series.

The API is a product of  `Kisters <https://www.kisters.de/en/>`_  and is called *KIWIS*. Hence, the code
would work on other deployments of this API as well. As VMM and HIC have each another deployment of the API,
the documentation could be slightly different for `VMM <https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo>`_
versus `HIC <https://www.waterinfo.be/tsmhic/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo>`_.

Introduction
------------

The waterinfo.be API uses a system of identifiers, called :code:`ts_id` to define individual time series.
For example, the identifier :code:`ts_id = 78073042` corresponds to the time series of air pressure data
for the measurement station in Liedekerke, with a 15 min time resolution. Hence, the :code:`ts_id` identifier
defines a variable of interest from a measurement station of interest with a specific frequency
(e.g. 15 min, hourly,…). The knowledge of the proper identifier is essential to be able to download
the corresponding data.

In order to get started, make sure to define the source of the data: VMM or HIC:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm") # look for data from VMM
    hic = Waterinfo("hic") # look for data from HIC

One of the reasons is that tokens are provided by them separately. If you have a token available, add this to the
initiation to make sure all session requests are using the token:

::

    from pywaterinfo import Waterinfo
    vmm_token = "DUMMY"
    vmm = Waterinfo("vmm",  token=vmm_token)

Download with known ts identifier
---------------------------------

In case you already know the :code:`ts_id` identifier that defines your time series, the class :class:`~pywaterinfo.Waterinfo` provides the method
:func:`~pywaterinfo.Waterinfo.get_timeseries_values` to download a specific period of the time series. For example, to download the air pressure time series data of Liedekerke with a 15 min resolution
(:code:`ts_id = 78073042`) for the first of January 2016:

::

    from pywaterinfo import Waterinfo
    vmm = Waterinfo("vmm")
    vmm.get_timeseries_values("78073042", start="2016-01-01", end="2016-01-02")

Mostly, you do not know these identifiers. Hence, to search for the required identifiers, different methods are
provided to support this, as described in the following sections.

The datetime inputs (:code:`start` and :code:`end`) are assumed to be 'UTC' by
default. To request data in another (supported) time zone (e.g. :code:`CET`, :code:`GMT`,
:code:`Etc/GMT+1`,...), add the :code:`timezone` parameter, e.g. :code:`timezone='CET'`.

.. warning::

    This behavior is different to the KIWIS API itself, which interprets the incoming
    date format always as :code:`CET`. Hence, requesting data to the REST API directly
    from '2019-05-01 14:00:00' with timezone 'UTC' will return data starting
    from '2019-05-01 12:00:00+00' (UTC). In the pywaterinfo package, the
    :code:`start` and :code:`end` parameters are assumed in the timezone of the request
    parameter :code:`timezone` (unless the :code:`start` and :code:`end` already contain
    time zone info).

Apart from the :code:`start` and :code:`end` configuration, the usage of the :code:`period` is a convenient
way of requesting time series. See the :func:`~pywaterinfo.Waterinfo.get_timeseries_values` for
more information and examples.

When interested in all available data of a time series (! watch out with credit limits) or using the start/end
of the time series in the request, one can find these in the metadata of a
time series as illustrated in the following example:

.. code:: python

    from pywaterinfo import Waterinfo

    hic = Waterinfo("hic")

    # Request the start/end of the time series
    station_metadata = hic.get_timeseries_list(ts_id = 51814010)
    start, end = station_metadata[["from", "to"]].values[0]

    # Get data from start of time series up to next two days
    df = hic.get_timeseries_values(51814010, start=start, period="P2D")

.. note::

    If you want 'naive' timestamps in the returned time series, use the :code:`tz_localize`
    function of Pandas, e.g. :code:`df["Timestamp"] = df["Timestamp"].dt.tz_localize(None)`.

Time series groups
------------------

A lot of the time series and stations are bundled in so-called :code:`timeseriesgroup_id`'s. They represent for example all
available station of rainfall at a given frequency (e.g. 15 Min). To get an overview of the available groups, use
the method :func:`~pywaterinfo.Waterinfo.get_group_list`, e.g. for the HIC stations:

::

    from pywaterinfo import Waterinfo
    hic = Waterinfo("hic")
    hic.get_group_list()

.. Note::
   A number of these group identifiers are described in the `available documentation <https://www.waterinfo.be/download/c4bc2c28-0251-40e3-8ecb-a139298597aa>`_ of VMM/HIC and
   are the preferred option to query for the provided variables. For an overview, see the
   :ref:`groupids` page.


Time series group data
-----------------------

To get all the available time series identifiers (:code:`ts_id`) within a given group, use the :func:`~pywaterinfo.Waterinfo.get_timeseries_value_layer`
method. It provides the metadata of these stations and (by default) the latest measured value. The group identifier for
conductivity measured by HIC is :code:`156173`:

::

    from pywaterinfo import Waterinfo
    hic = Waterinfo("hic")
    hic.get_timeseries_value_layer(timeseriesgroup_id="156173")

Multiple identifiers can be combined in a single statement:

::

    from pywaterinfo import Waterinfo
    hic = Waterinfo("hic")
    # combine oxygen and conductivity in a single call
    hic.get_timeseries_value_layer(timeseriesgroup_id="156207,156173")

.. note::

    When requesting only a subset of the fields using :code:`returnfields`, the resulting dataframe
    still contains a lot of metadata fields added by default. To exclude these in the respond,
    use the :code:`metadata` parameter equal to :code:`False`. For example:

    ::

        water_level = vmm.get_timeseries_value_layer("192780",
            returnfields="timestamp,ts_value",
            metadata="false")


Search identifier based on parameter or station name
----------------------------------------------------

In the situation you are looking for the identifiers of all measured parameters at a station or all the
stations measuring a given parameter, use the :func:`~pywaterinfo.Waterinfo.get_timeseries_list` method.
It supports wildcards and supports looking based on station information, parameter information or a combination of both:

::

        vmm = Waterinfo("vmm")
        # for given station ME09_012, which time series are available?
        vmm.get_timeseries_list(station_no="ME09_012")
        # for a given parameter PET, which time series are available?
        vmm.get_timeseries_list(parametertype_name="PET")

An example use case is to get the available parameters (in waterinfo also called ``stationparameter``) at a given station? As pywaterinfo returns a Pandas DataFrame, combine pywaterinfo with the functionalities from Pandas (e.g. ``unique`` method):

::

        vmm = Waterinfo("vmm")
        # for station L11_518, which station parameters are available?
        station_l11_518 = vmm.get_timeseries_list(station_no="L11_518",
                                                  returnfields="ts_id,station_name,stationparameter_longname")
        station_l11_518["stationparameter_longname"].unique()


Custom queries
--------------

The `VMM <https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo>`_
and `HIC <https://www.waterinfo.be/tsmhic/KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&request=getrequestinfo>`_ APIs
provide more API paths. Whereas no specialized functions are available, use the :func:`~pywaterinfo.Waterinfo.request_kiwis` method
to do custom calls to the KIWIS API. For example, using the :code:`getStationList` query for stations starting with a :code:`P`:

::

    vmm = Waterinfo("vmm")
    vmm.request_kiwis({"request": "getStationList", "station_no": "P*"})
