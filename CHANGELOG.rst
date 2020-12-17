=========
Changelog
=========

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
