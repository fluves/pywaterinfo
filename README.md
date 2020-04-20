# pywaterinfo

Python package to download time series data from waterinfo.be

![Python package](https://github.com/fluves/pywaterinfo/workflows/Python%20package/badge.svg?branch=master)

## Description

pywaterinfo facilitates access to [waterinfo.be](https://www.waterinfo.be/), a website managed by the [Flanders Environment Agency (VMM)](https://en.vmm.be/) and [Flanders Hydraulics Research](https://www.waterbouwkundiglaboratorium.be/). The website provides access to real-time water and weather related environmental variables for Flanders (Belgium), such as rainfall, air pressure, discharge, and water level. The package provides functions to search for stations and variables, and download time series.

## Installation

... TODO

## Example

... TODO


## Contribute

... TODO

---------------------------

A `.pre-commit-config.yaml` file was generated inside your project but in order to make sure the hooks will run, please don't forget to install the `pre-commit` package:

  cd pywaterinfo
  >>> it is a good idea to create and activate a virtualenv here
  pip install pre-commit
  pre-commit install
  >>> another good idea is update the hooks to the latest version
  >>> pre-commit autoupdate

You might also consider including similar instructions in your docs, to remind the contributors to do the same.

---------------------------

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

```
# after git clone of empty repo `pywaterinfo`:
putup --pyproject --markdown --pre-commit --tox --travis --force pywaterinfo
```


## Acknowledgements

The package development and maintenance is supported by [Fluves](https://fluves.com/).
Part of the initial development of this package has been supported by [VITO](https://vito.be).

<p align="center">
  <img src="./docs/_static/img/logo_fluves.png">
  <img src="./docs/_static/img/logo_vito.png">
</p>
