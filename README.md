# pywaterinfo

Python package to download time series data from waterinfo.be and hydrometrie.wallonie.be.

![Python package](https://github.com/fluves/pywaterinfo/actions/workflows/ci.yml/badge.svg?branch=master)

## Description

pywaterinfo facilitates access to [waterinfo.be](https://www.waterinfo.be/), a website managed by the [Flanders Environment Agency (VMM)](https://en.vmm.be/) in combination with [Flanders Hydraulics Research](https://www.waterbouwkundiglaboratorium.be/) and [L'hydrométrie en Wallonie](https://hydrometrie.wallonie.be/) managed by [Service public de Wallonie](https://spw.wallonie.be/). The websites provide access to real-time water and weather related environmental variables for Flanders and Wallonia respectively (Belgium), such as rainfall, air pressure, discharge, and water level. The package provides functions to search for stations and variables, and
to download time series and raster data.

Check out the [documentation website](https://fluves.github.io/pywaterinfo/) for more information.

## Installation

```
pip install pywaterinfo
```

### Extra dependencies

- A cached connection can also be made to make sure consecutive calls for the
  same data are stored in a local cache. Install the extra dependencies using;

  ```
  pip install pywaterinfo[cache]
  ```


## Example

To initialize data requests from VMM, setup the `Waterinfo` class with `vmm` as input:

```python
from pywaterinfo import Waterinfo
vmm = Waterinfo("vmm")
```

The time series provided by waterinfo are all defined by a unique identifier called `ts_id`. Each combination of a given __variable__ (e.g. air pressure)
measured at a given __location__ (e.g. Overpelt) with a certain __frequency__ (e.g. 15min) is defined by an `ts_id` identifier. Using such an identifier,
one can download the data of a given period with the command `get_timeseries_values()`. For example, the 15min air pressure time series
at Overpelt has identifier `ts_id = 78124042`. To get last day of data for the time series with ID `78124042`:

```python
df = vmm.get_timeseries_values(78124042, period="P1D")
```

pywaterinfo returns the data as a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/index.html), which provides functionlities to plot and manipulate the time series.

Requesting data from HIC is very similar:

```python
hic = Waterinfo("hic")
```

Get last day of data for the time series with ID `39496010`, corresponding to high-resolution (5min) conductivity measurements in Dendermonde:

```python
df = hic.get_timeseries_values(ts_id="39496010", period="P1D")
```

Requesting data from SPW, L'hydrométrie en Wallonie, is also similar:

```python
spw = Waterinfo("spw")
df = spw.get_timeseries_values(ts_id="235519010", period="P1D")
```

Next to the request of time series data for a given time series identifier, other
requests are supported as well. These functions provide multiple ways to search for the
`ts_id` you need to download certain data. See the [documentation website](https://fluves.github.io/pywaterinfo/) for more info.

## Note on restrictions of the downloads

### waterinfo.be

The amount of data downloaded from waterinfo.be is limited via a credit system. You do not need to get a token right away to download data. For limited and irregular downloads, a token will not be required.

When you require more extended data requests, please request a download token from the waterinfo.be site administrators via the e-mail address <hydrometrie@waterinfo.be> with a statement of which data and how frequently you would like to download data. You will then receive a client-credit code that can be used to obtain a token that is valid for 24 hours, after which the token can be refreshed with the same client-credit code. The handling of this token is done by
the package itself, but it is important to use the code when initializing the `Waterinfo` instance. For example, using a VMM token:

```
from pywaterinfo import Waterinfo
vmm_token = "YOUR TOKEN CODE"
vmm = Waterinfo("vmm",  token=vmm_token)
```

### hydrometrie.wallonie.be

When restricted by the number of data downloads at hydrometrie.wallonie.be, check out the contact form enlisted on the [hydrometrie.wallonie.be website](https://hydrometrie.wallonie.be/home/services/demande-dun-compte.html) for more information.


## Contribute

Want to contribute code or functionalities to the `pywaterinfo` package? Great news! Check out the [contributing guidelines](https://fluves.github.io/pywaterinfo/contributing.html) and the [development guidelines](https://fluves.github.io/pywaterinfo/contributing.html#development-guidelines) in the documentation website.

## Acknowledgements

The package development and maintenance is supported by [Fluves](https://fluves.com/).
Part of the initial development of this package has been supported by [VITO](https://vito.be).

<p align="center">
  <img src="https://static.s3.nl-ams.scw.cloud/Fluves_wordmark_black.svg" width="150px", alt="Logo Fluves">
  <img src="https://vito.be/themes/custom/vitotheme/logo.svg" width="120px" alt="Logo VITO">
</p>

This package is just a small wrapper around waterinfo.be to facilitate researchers and other stakeholders in downloading the data from [waterinfo.be](http://www.waterinfo.be) and [Service public de Wallonie](https://spw.wallonie.be/). The availability of the data on waterinfo.be data is made possible by *de Vlaamse Milieumaatschappij, Waterbouwkundig Laboratorium, Maritieme Dienstverlening & Kust, Waterwegen en Zeekanaal NV and De Scheepvaart NV*, whereas the data on hydrometrie.wallonie.be is made possible by [Service public de Wallonie](https://spw.wallonie.be/).

## Meta

* We welcome [contributions](https://fluves.github.io/pywaterinfo/contributing.html) including bug reports.
* License: MIT
* Please note that this project is released with a [Contributor Code of Conduct](https://fluves.github.io/pywaterinfo/contributing.html#code-of-conduct). By participating in this project you agree to abide by its terms.
* For those wondering... The name is a reference to the original scope of the package, i.e. waterinfo.be. The addition of hydrometrie.wallonie.be was a logical addition in terms of technology and scope (belgium). Still, the name of the package is kept pywaterinfo.

This project has been set up using PyScaffold 3.2.3. For details and usage information on PyScaffold see https://pyscaffold.org/.
