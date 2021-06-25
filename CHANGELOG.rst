=========
Changelog
=========

Version 0.4.0
=============

- Switch local caching (#32) to temporary os directoy instead of project directory
- Extend example/documentation:
    - Add example on how to request start/end date of a time series metadata (#33)

Version 0.3.1
=============

- Extend example/documentation:
    - Add caching page to index of manual pages

Version 0.3.0
=============

- Add local caching of API requests using the `requests-cache` package.
- Adjust root URL for HIC based API calls according to online documentation https://hicws.vlaanderen.be/.
- User can use custom time zone instead of UTC as default.
- Extend examples/documentation for specific:
    - Limit the returned fields of `get_timeseries_value_layer` with `metadata=False`.
    - Add example on how to request tide numbers for high/low tide data.

Version 0.2.2
=============

Fix token handling for HIC data requests.

Version 0.2.1
=============

Hot fix on token handling (Thanks to Erik Bollen for reporting).

Version 0.2.0
=============

Add support for SSL certificate handling.

Version 0.1.1
=============

This version provides a first implementation wrapping the API provided by `waterinfo.be <https://www.waterinfo.be/>`_. The package provides a minimal
wrapper with the aim to find and download time series data and returns it as Pandas DataFrame. The latter enables methods for plotting and analysis.

- Add Waterinfo class with base HTTP call method `request_kiwis`
- Handle tokens automatically
- Provide Python API equivalent for `getTimeseriesValues`, `getTimeseriesValueLayer`, `getGroupList` and `getTimeseriesList`
- Create documentation website with SPhinx, unit tests using pytest, doctests
- Setup of the CI using Github actions
