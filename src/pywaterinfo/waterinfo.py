import datetime
import logging
import pkg_resources
import re

import pandas as pd
import requests

"""
INFO:

https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters& \
    type=QueryServices&format=html&request=getrequestinfo
other KIWIS-python clients:
    - https://github.com/amacd31
    - https://gitlab.com/kisters/kisters.water.time_series
"""


VMM_BASE = "https://download.waterinfo.be/tsmdownload/KiWIS/KiWIS"
VMM_AUTH = "http://download.waterinfo.be/kiwis-auth/token"
HIC_BASE = "https://www.waterinfo.be/tsmhic/KiWIS/KiWIS"
HIC_AUTH = "https://hicwsauth.vlaanderen.be/auth"
DATA_PATH = pkg_resources.resource_filename(__name__, "/data")

# Custom hard-coded fix for the decoding issue #1 of given returnfields
DECODE_ERRORS = ["AV Quality Code Color", "RV Quality Code Color"]

logger = logging.getLogger(__name__)


class KiwisException(Exception):
    """Raised when the KIWIS calls contain error"""

    pass


class WaterinfoException(Exception):
    """Raised when the Waterinfo data request inputs are wrong"""

    pass


class Waterinfo:
    def __init__(self, provider: str = "vmm", token: str = None):
        """Request data from waterinfo.be

        Parameters
        ----------
        provider : vmm | hic
            Define the origin of the data on waterinfo you're looking for. Either
            provided by VMM (vmm) or HIC (hic)
        token : str
            Token as provided by VMM on project-level.
        """

        # set the base string linked to the data provider
        if provider == "vmm":
            self._base_url = VMM_BASE
            self._auth_url = VMM_AUTH
            self._datasource = "1"
        elif provider == "hic":
            self._base_url = HIC_BASE
            self._auth_url = HIC_AUTH
            self._datasource = "4"
        else:
            raise WaterinfoException("Provider is either 'vmm' or 'hic'.")

        self._request = requests.Session()

        self.__default_args = {
            "service": "kisters",
            "type": "QueryServices",
            "format": "json",
            "datasource": self._datasource,
            "timezone": "UTC",
        }

        self._token_header = None
        if token:
            res = requests.post(
                self._auth_url,
                headers={
                    "Authorization": f"Basic {token}",
                    "scope": "none",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "charset": "UTF-8",
                },
                data={"grant_type": "client_credentials"},
            )
            res.raise_for_status()
            res_parsed = res.json()
            self._token_header = {
                "Authorization": f"{res_parsed['token_type']} "
                f"{res_parsed['access_token']}"
            }
            expires_in = res_parsed["expires_in"]
            expires_on = datetime.datetime.now() + datetime.timedelta(
                seconds=expires_in
            )
            logging.info(f"Current token expires on {expires_on}")

        # request the API info from the waterinfo KIWIS service itself
        query_param = {"request": "getRequestInfo"}

        headers = dict()
        if self._token_header:
            headers.update(self._token_header)
        info, _ = self.request_kiwis(query_param, headers=headers)
        self._kiwis_info = info[0]["Requests"]

        self._default_params = ["format", "returnfields", "request"]

    def __repr__(self):
        return f"<{self.__class__.__name__} object, " f"Query from {self._base_url!r}>"

    def request_kiwis(self, query: dict, headers: dict = None) -> dict:
        """ http call to waterinfo.be KIWIS API

        General call used to request information and data from waterinfo.be, providing
        error handling and json parsing. The service, type, format (json),
        datasource and timezone (UTC) are provided by default (but can be overridden
        by adding them to the query).

        Whereas specific methods are provided to support the queries getTimeseriesList,
        getTimeseriesValues, getTimeseriesValueLayer and getGroupList; this method
        can be used to use the other available queries as well.

        Parameters
        ----------
        query : dict
            list of query options to be used together with the base string
        headers : dict
            authentication header for the call

        Returns
        -------
        parsed json object, full HTTP response

        Examples
        --------
        >>> from pywaterinfo import Waterinfo
        >>> vmm = Waterinfo("vmm")
        >>> # get the API info/documentation from kiwis
        >>> data, res = vmm.request_kiwis({"request": "getRequestInfo"})
        >>> data        #doctest: +ELLIPSIS
        [{'Title': 'KISTERS QueryServices - Request Inform...file'}}}}}}]
        >>> res.status_code
        200
        >>> # get the timeseries data from last day from time series 78124042
        >>> data, res = vmm.request_kiwis({"request": "getTimeseriesValues",
        ...                                "ts_id": "78124042",
        ...                                "period": "P1D"})
        >>> data        #doctest: +ELLIPSIS
        [{'ts_id': '78124042'...]]}]
        >>> # get all stations starting with a P in the station_no
        >>> data, res = vmm.request_kiwis({"request": "getStationList",
        ...                                "station_no": "P*"})
        >>> data        #doctest: +ELLIPSIS
        [['station_name'...]]
        """
        # query input checks: valid parameters and formatting of the parameters period,
        # dateformat, returnfields
        query = {key.lower(): value for (key, value) in query.items()}
        if query["request"] != "getRequestInfo":
            self._check_query_parameters(query)
        if "period" in query.keys():
            self._check_period_format(query["period"])
        if "dateformat" in query.keys():
            self._check_return_date_format(query["dateformat"], query["request"])
        if "returnfields" in query.keys():
            self._check_return_fields_format(query["returnfields"], query["request"])

        query.update(self.__default_args)
        if not headers:
            headers = dict()
        if self._token_header:
            headers.update(self._token_header)
        res = self._request.get(self._base_url, params=query, headers=headers)

        if res.status_code != requests.codes.ok:
            raise KiwisException(
                f"Waterinfo call returned {res.status_code} error"
                f"with the message {res.content}"
            )
        logging.info(f"Successful waterinfo API request with call {res.url}")

        parsed = res.json()
        if (
            type(parsed) is dict
            and "type" in parsed.keys()
            and parsed["type"] == "error"
        ):
            raise KiwisException(
                f"Waterinfo API returned an error:\n\tCode: "
                f"{parsed['code']}\n\tMessage: {parsed['message']}"
            )

        return parsed, res

    def _check_query_parameters(self, query):
        """Check if all given parameters in the query are known to
        the KIWIS webservice"""

        request = query["request"]
        supported_parameters = set(
            self._kiwis_info[request]["QueryFields"]["Content"].keys()
        )
        optional_parameters = set(
            self._kiwis_info[request]["Optionalfields"]["Content"].keys()
        )

        for (parameter, _) in query.items():
            if parameter not in (
                supported_parameters | optional_parameters | set(self._default_params)
            ):
                raise WaterinfoException(
                    f"Parameter '{parameter}' not in requestInfo for {request}. Check "
                    f"{self._base_url}?service=kisters&type=queryServices"
                    f"&request=getRequestInfo "
                    f"for an overview of the documentation."
                )

    @staticmethod
    def _check_period_format(period_string):
        """Check period string format

        Check if the format of the period is conform the specifications of
        the KIWIS webservice definition.

        Parameters
        ----------
        period_string: str
            Input string according to format required by waterinfo:
            The period string is provided as P#Y#M#DT#H#M#S, with P defines `Period`,
            each # is an integer value and the codes define the number of...
            Y - years
            M - months
            D - days
            T required if information about sub-day resolution is present
            D - days
            H - hours
            M - minutes
            S - seconds
            Instead of D (days), the usage of W - weeks is possible as well
            Examples of valid period strings: P3D, P1Y, P1DT12H, PT6H, P1Y6M3DT4H20M30S.

        Returns
        -------
        str period string itself if valid

        Examples
        --------
        >>> _check_period_format("P2DT6H") # period of 2 days and 6 hours
        >>> _check_period_format("P3D") # period of 3 days
        """
        pattern = re.compile(
            "^P(?=[0-9]+|T)[0-9]*Y?(?!M)[0-9]*M?(?![DW])[0-9]*[D,W]?(T)"
            "?(?(1)(?![H])[0-9]*H?(?![M])[0-9]*M?(?![S])[0-9]*S?|)$"
        )
        valid = pattern.match(period_string)

        if not valid:
            raise WaterinfoException(
                "The period string is not a valid expression. Examples of"
                " valid expressions are"
                " P3D, P1Y, P1DT12H, PT6H, P1Y6M3DT4H20M30S"
            )
        return period_string

    def _check_return_date_format(self, dateformat, request="getTimeseriesValues"):
        """Check if the requested output date format is known to the KIWIS webservice
        """
        supported_formats = set(
            self._kiwis_info[request]["Dateformats"]["Content"].keys()
        )
        if dateformat not in supported_formats:
            raise WaterinfoException(
                f"The requested returned datetime {dateformat} format is not valid "
                f"as KIWIS input. The supported formats are {supported_formats} or "
                f"check {self._base_url}?service=kisters&type=queryServices&"
                f"request=getRequestInfo for an overview of the documentation."
            )

    def _check_return_fields_format(self, return_fields, request="getTimeseriesValues"):
        """Check if the requested return_fields are known to the KIWIS webservice"""
        return_fields = set(return_fields.split(","))  # user requested
        supported_fields = set(
            self._kiwis_info[request]["Returnfields"]["Content"].keys()
        )  # api supported

        if not return_fields <= supported_fields:
            invalid_fields = return_fields - supported_fields
            raise WaterinfoException(
                f"Returnfield(s) {invalid_fields} not in requestInfo for {request}. "
                f"The supported formats are {supported_fields} or check "
                f"{self._base_url}?service=kisters&type=queryServices&"
                f"request=getRequestInfo for an overview of the documentation."
            )

    @staticmethod
    def _parse_date(input_datetime):
        """Evaluate date and transform to format accepted by KIWIS API

        Dates can be specified on a courser-than-day basis, but will always be
        transformed to start of... (year, month,...). For example, '2007' will be
        translated to '20170101 00:00'.

        Note, the input datetime of the KIWIS API is always CET (and is not tz-aware),
        but we normalize everything to UTC. Hence, we interpret the user input as UTC,
        provide the input to the API as CET and request the returned
        output data as UTC.

        Parameters
        ----------
        input_datetime : str
            datetime string
        """
        return (
            pd.to_datetime(input_datetime, utc=True)
            .tz_convert("CET")
            .strftime("%Y-%m-%d %H:%M:%S")
        )

    def _parse_period(self, start=None, end=None, period=None):
        """Check the from/to/period arguments when requesting (valid for
        getTimeseriesValues and getGraph)

        Handle the information of provided date information on the period and provide
        feedback to the user. Valid combinations of the arguments are:
        from/to, from/period, to/period, period, from

        - from + to: will return the requested range
        - from + period: will return the given period starting at the from date
        - to + period: will return the given period backdating from the to date
        - period: will return the given period backdating from the current system time
        - from:	will return all data starting at the given from date until
          the current system time

        Parameters
        ----------
        start : str
            valid datetime string representation as defined in the KIWIS getRequestInfo
        end : str
            valid datetime string representation as defined in the KIWIS getRequestInfo
        period: str
            @param period input string according to format required by waterinfo

        Returns
        -------
        dict with the relevant period/date information
        """

        # if none of 3 provided, error
        if (not start) and (not end) and (not period):
            raise WaterinfoException(
                "Date information should be provided by a combination of 2 "
                "parameters out of from / to / period"
            )

        # if all 3 provided, error
        if start and end and period:
            raise WaterinfoException(
                "Date information should be provided by a combination of maximum 2 "
                "parameters out of from / to / period"
            )

        # if only 'to' provided, error
        if (not start) and end and (not period):
            raise WaterinfoException(
                "Date information should be provided by providing a "
                "from or period input"
            )

        period_info = dict()

        if start:
            period_info["from"] = self._parse_date(start)
        if end:
            period_info["to"] = self._parse_date(end)
        if period:
            period_info["period"] = self._check_period_format(period)

        return period_info

    def get_timeseries_values(
        self,
        ts_id=None,
        timeseriesgroup_id=None,
        period=None,
        start=None,
        end=None,
        **kwargs,
    ):
        """Get time series data from waterinfo.be

        Using the ts_id codes or group identifiers and by providing a given date
        period, download the corresponding time series from the waterinfo.be website.
        Each identifier ts_id corresponds to a given variable-location-frequency
        combination (e.g. precipitation, Waregem, daily). When interested in daily,
        monthly, yearly aggregates look for these identifiers in order to overcome
        too much/large requests.

        Note: The usage of 'start' and 'end' instead of the API default from/to is done
        to avoid the usage of from, which is a protected name in Python.

        Parameters
        ----------
        ts_id : str
            single or multiple ts_id values, comma-separated
        timeseriesgroup_id : str
            single or multiple group identifiers, comma-separated
        period : str
            input string according to format required by waterinfo: the period string
            is provided as P#Y#M#DT#H#M#S, with P defines `Period`, each # is an
            integer value and the codes define the number of...
            Y - years M - months D - days T required if information about sub-day
            resolution is present H - hours D - days M - minutes S - seconds Instead
            of D (days), the usage of W - weeks is possible as well.
            Examples of valid period strings: P3D, P1Y, P1DT12H, PT6H, P1Y6M3DT4H20M30S.
        start : datetime | str
            Either Python datetime object or a string which can be interpreted
            as a valid Timestamp.
        end : datetime | str
            Either Python datetime object or a string which can be interpreted
            as a valid Timestamp.
        kwargs :
            Additional query parameter options as documented by KIWIS waterinfo API,
            see `API docoumentation <https://download.waterinfo.be/tsmdownload/
            KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&
            request=getrequestinfo>`_

        Returns
        -------
        pd.DataFrame
            DataFrame with for time series data and datetime in UTC.

        Examples
        --------
        >>> from pywaterinfo import Waterinfo
        >>> vmm = Waterinfo("vmm")
        >>>
        >>> # get last day of data for the time series with ID 78124042
        >>> df = vmm.get_timeseries_values(78124042, period="P1D")
        >>>
        >>> # get last day data of time series with ID 78124042 with subset of columns
        >>> my_columns = ("Timestamp,Value,Interpolation Type,Quality Code,Quality"
        ...               " Code Name,Quality Code Description")
        >>> df = vmm.get_timeseries_values(78124042, period="P1D",
        ...                                returnfields=my_columns)
        >>>
        >>> # get the data for ts_id 60992042 and 60968042 (Moerbeke_P and Waregem_P)
        >>> # for 20190502 till 20190503
        >>> # Note: UTC as time unit is used as input and asked as output by default
        >>> df = vmm.get_timeseries_values("60992042,60968042",
        ...                           start="20190502", end="20190503")
        >>>
        >>> # get the data for all stations from groups 192900 (yearly rain sum)
        >>> # and 192895 (yearly discharge average) for the last 2 years
        >>> df = vmm.get_timeseries_values(timeseriesgroup_id="192900,192895",
        ...                                period="P2Y")  # doctest: +SKIP
        >>>
        >>> hic = Waterinfo("hic")
        >>>
        >>> # get last day of data for the time series with ID 44223010
        >>> df = hic.get_timeseries_values(ts_id="44223010", period="P1D")
        >>>
        >>> # get last day data of time series with ID 44223010 with subset of columns
        >>> df = hic.get_timeseries_values(ts_id="44223010", period="P1D",
        ...          returnfields="Timestamp,Value,Interpolation Type,Quality Code")
        """
        # check the period information
        period_info = self._parse_period(start=start, end=end, period=period)

        # add either ts_id or timeseriesgroup_id
        if ts_id and timeseriesgroup_id:
            raise WaterinfoException(
                "A combination of ts_id and timeseriesgroup_id is not possible, "
                "use one of these three"
            )
        if not ts_id and not timeseriesgroup_id:
            raise WaterinfoException("Either ts_id or timeseriesgroup_id is required.")

        # collect all possible returnfields
        returnfields = self._kiwis_info["getTimeseriesValues"]["Returnfields"][
            "Content"
        ].keys()
        all_returnfields = [
            field for field in returnfields if field not in DECODE_ERRORS
        ]

        query_param = dict(
            request="getTimeseriesValues",
            ts_id=ts_id,
            timeseriesgroup_id=timeseriesgroup_id,
            returnfields=",".join(all_returnfields),
        )
        query_param.update(period_info)
        query_param.update(kwargs)

        data, response = self.request_kiwis(query_param)

        # All metadata of time series (except of columns, data and rows) converted
        # to additional columns in df in order to concat all of them while keeping the
        # information to trace the origin
        time_series = []
        for section in data:
            df = pd.DataFrame(section["data"], columns=section["columns"].split(","))
            for key_name in section.keys():
                if key_name not in ("columns", "data", "rows"):
                    df[key_name] = section[key_name]
            # convert datetime objects to Pandas timestamp
            if "Timestamp" in df.columns:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            time_series.append(df)

        return pd.concat(time_series)

    def get_timeseries_value_layer(
        self, timeseriesgroup_id=None, ts_id=None, bbox=None, **kwargs
    ):
        """Get metadata and last measured value for group of stations

        Either ts_id, timeseriesgroup_id or bbox can be used to request data. The
        function provides metadata and the last measured value for the group of
        ids/stations.

        Note, by using an additional 'date' argument, the data value of another moment
        can be requested as well.

        Parameters
        ----------
        ts_id : str
            single or multiple ts_id values, comma-separated
        timeseriesgroup_id : str
            single or multiple group identifiers, comma-separated
        bbox :
            Comma separated list with four values in order min_x, min_y, max_x, max_y;
            use 'crs' parameter to choose between local and global coordinates. fields
            stationparameter_no and ts_shortname are required for bbox; the function
            will select 0 or 1 timeseries per station in the area according to filters
        kwargs :
            Additional query parameter options as documented by KIWIS waterinfo API, see
            `API docoumentation <https://download.waterinfo.be/tsmdownload/
            KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&
            request=getrequestinfo>`_

        Returns
        -------
        pd.DataFrame
            DataFrame with for each time series in the group a row containing
            measurement and metadata

        Examples
        --------
        >>> from pywaterinfo import Waterinfo
        >>> vmm = Waterinfo("vmm")
        >>>
        >>> # get the metadata and last measured value on a single time series
        >>> df = vmm.get_timeseries_value_layer(ts_id=78124042)
        >>>
        >>> # get the metadata and last measured value of all members of a
        >>> # time series group
        >>> df = vmm.get_timeseries_value_layer(timeseriesgroup_id=192928)
        >>>
        >>> # get the measured value of all members of a time series group on
        >>> # a given time stamp
        >>> df = vmm.get_timeseries_value_layer(timeseriesgroup_id=192928,
        ...                                     date="20190501")
        >>>
        >>> hic = Waterinfo("hic")
        >>>
        >>> # get the metadata and last measured value of the oxygen concentration
        >>> # (group id 156207) and conductivity (group id 156173) combined
        >>> df = hic.get_timeseries_value_layer(timeseriesgroup_id="156207,156173")
        """
        # hard coded set of metadata return fields as only in description
        # field of queryinfo
        md_returnfields = (
            "ts_id,ts_path,ts_name,ts_shortname,station_no,station_id,station_name,"
            "stationparameter_name,stationparameter_no,stationparameter_longname,"
            "ts_unitname,ts_unitsymbol,parametertype_id,parametertype_name,ca_sta"
        )
        ca_sta_returnfields = "dataprovider"

        # add either ts_id, timeseriesgroup_id or bbox to the query
        if (
            (ts_id and timeseriesgroup_id and bbox)
            or (ts_id and timeseriesgroup_id)
            or (timeseriesgroup_id and bbox)
            or (ts_id and bbox)
        ):
            raise WaterinfoException(
                "A combination of ts_id, timeseriesgroup_id or bbox not possible, "
                "use one of these three"
            )
        query_param = dict(
            request="getTimeseriesValueLayer",
            metadata="TRUE",
            md_returnfields=md_returnfields,
            ca_sta_returnfields=ca_sta_returnfields,
            ts_id=ts_id,
            timeseriesgroup_id=timeseriesgroup_id,
            bbox=bbox,
        )

        query_param.update(kwargs)
        data, response = self.request_kiwis(query_param)

        return pd.DataFrame(data)

    def get_group_list(self, group_name=None, group_type=None, **kwargs):
        """Get a list of time series and station groups

        The function provides the existing group identifiers. These group_ids enable
        the user to request all values of a given group at the same time (method
        `get_timeseries_value_layer` or `get_timeseries_values`).

        Parameters
        ----------
        group_name : str
            Name of the time series group, can contain wildcards, e.g. '*Download*'
        group_type : 'station' | 'parameter' | 'timeseries'
            Specify the type station, parameter or timeseries
        kwargs :
            Additional queryfields as accepted by the KIWIS call getGroupList, see
            `API docoumentation <https://download.waterinfo.be/tsmdownload/
            KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&
            request=getrequestinfo>`_

        Returns
        -------
        pd.DataFrame
            DataFrame with an overview of the groups provided by the API

        Examples
        --------
        >>> from pywaterinfo import Waterinfo
        >>> vmm = Waterinfo("vmm")
        >>>
        >>> # all available groupid's provided by VMM
        >>> df = vmm.get_group_list()
        >>>
        >>> # all available groupid's provided by VMM that represent a time series
        >>> df = vmm.get_group_list(group_type='timeseries')
        >>>
        >>> # all available groupid's  provided by VMM containing 'Download' in
        >>> # the group name
        >>> df = vmm.get_group_list(group_name='*Download*')
        >>>
        >>> hic = Waterinfo("hic")
        >>>
        >>> # all available groupid's provided by HIC
        >>> df = hic.get_group_list()
        """
        if group_type and group_type not in ["station", "parameter", "timeseries"]:
            raise WaterinfoException(
                "Invalid group_type, use 'station', 'parameter' or 'timeseries'"
            )

        query_param = dict(
            request="getGroupList", group_name=group_name, group_type=group_type
        )

        query_param.update(kwargs)
        data, response = self.request_kiwis(query_param)

        return pd.DataFrame(data[1:], columns=data[0])

    def get_timeseries_list(
        self, station_no=None, stationparameter_name=None, **kwargs
    ):
        """Get time series at given station an/or time series which provide
        certain parameter

        The station_no and stationparameter_name are provided as arguments, as these
        represent our typical use cases: station_no and stationparameter_name are shown
        on the waterinfo.be download pages as respectively the 'station_number' and
        'parameter' column.

        By default all returnfields are provided in the returned dataframe, but this
        can be overridden by the user by providing the returnfields as an additional
        argument.

        Parameters
        ----------
        station_no : str
            single or multiple station_no values, comma-separated
        stationparameter_name : str
            single or multiple stationparameter_name values, comma-separated
        kwargs :
            Additional queryfields as accepted by the KIWIS call getTimeseriesList, see
            `API docoumentation <https://download.waterinfo.be/tsmdownload/
            KiWIS/KiWIS?service=kisters&type=QueryServices&format=html&
            request=getrequestinfo>`_

        Returns
        -------
        pd.DataFrame
            DataFrame with each row the time series metadata

        Examples
        --------
        >>> from pywaterinfo import Waterinfo
        >>> vmm = Waterinfo("vmm")
        >>>
        >>> # for given station ME09_012, which time series are available?
        >>> df = vmm.get_timeseries_list(station_no="ME09_012") # doctest: +SKIP
        >>>
        >>> # for a given parameter PET, which time series are available?
        >>> df = vmm.get_timeseries_list(parametertype_name="PET") # doctest: +SKIP
        >>>
        >>> # for a given parameter PET and station ME09_012, which time series
        >>> # are available?
        >>> df = vmm.get_timeseries_list(parametertype_name="PET",
        ...                              station_no="ME09_012")
        >>>
        >>> # for a given parametertype_id 11502, which time series are available?
        >>> df = vmm.get_timeseries_list(parametertype_id="11502")
        >>>
        >>> # only interested in a subset of the returned columns: ts_id, station_name,
        >>> # stationparameter_longname
        >>> df = vmm.get_timeseries_list(parametertype_id="11502",
        ...                returnfields="ts_id,station_name,stationparameter_longname")
        >>>
        >>> hic = Waterinfo("hic")
        >>>
        >>> # for a given parameter EC, which time series are available?
        >>> df = hic.get_timeseries_list(parametertype_name="EC")
        >>>
        >>> # for a given station plu03a-1066, which time series are available?
        >>> df = hic.get_timeseries_list(station_no="plu03a-1066")
        """
        all_returnfields = list(
            self._kiwis_info["getTimeseriesList"]["Returnfields"]["Content"].keys()
        )
        # custom-fix: remove 'ts_clientvalue##' and 'datacart' from returnfields
        # as these provide error
        all_returnfields = [
            field
            for field in all_returnfields
            if field not in ["ts_clientvalue##", "datacart"]
        ]

        query_param = dict(
            request="getTimeseriesList",
            station_no=station_no,
            stationparameter_name=stationparameter_name,
            returnfields=",".join(all_returnfields),
        )

        query_param.update(kwargs)
        data, response = self.request_kiwis(query_param)

        if data[0] == "No matches.":
            return pd.DataFrame([])
        else:
            return pd.DataFrame(data[1:], columns=data[0])
