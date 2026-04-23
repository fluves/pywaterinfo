.. _groupids:

===================
Timeseriesgroup_ids
===================

Introduction
------------

For a number of time series, the VMM and HIC provide the group identifiers in the online
`available documentation <https://www.waterinfo.be/download/c4bc2c28-0251-40e3-8ecb-a139298597aa>`_.
These identifiers are the preferred source to query the enlisted variables.

.. note:: When you only require yearly aggregations, check for a time series with a corresponding
   frequency to overcome large data queries as much as possible.


VMM
---

For the VMM, the list of available group identifiers (date: 2017-10-01) are provided in the following table.

.. Caution:: These identifiers are not described as stable identifiers and can change in time!

.. csv-table:: VMM published timeseriesgroup identifiers
   :header: "variable (nl)", "frequency_nl", "timeseriesgroup_id", "variable (en)", "frequency (en)"

      afvoer, 15min, 192786, discharge, 15min
      afvoer, uur, 192892, discharge, hour
      afvoer, dag, 192893, discharge, day
      afvoer, maand, 192894, discharge, month
      afvoer, jaar, 192895, discharge, year
      bodem_verzadiging, 15min, 192929, soil_saturation, 15min
      bodem_vocht, 15min, 192928, soil_moisture, 15min
      dauwpunt_temperatuur, 15min, 192923, dew_point_temperature, 15min
      geleidbaarheid (permanent meetnet), 15min, 383065, conductivity (continuous network), 15min
      geleidbaarheid (project), 15min, 381863, conductivity (project based), 15min
      grondtemperatuur, 15min, 192924, ground_temperature, 15min
      grondwarmte, 15min, 192916, ground_heat, 15min
      instraling, 15min, 192920, irradiance, 15min
      luchtdruk, 15min, 192918, air_pressure, 15min
      luchttemperatuur175cm, 15min, 192922, air_temperature_175cm, 15min
      neerslag, 1m, 199792, rainfall, 1min
      neerslag, 15min, 192896, rainfall, 15min
      neerslag, uur, 192897, rainfall, hour
      neerslag, dag, 192898, rainfall, day
      neerslag, maand, 192899, rainfall, month
      neerslag, jaar, 192900, rainfall, year
      relatieve_vochtigheid, 15min, 192919, relative_humidity, 15min
      verdamping_monteith, 15min, 192927, evaporation_monteith, 15min
      verdamping_monteith, dag, 295480, evaporation_monteith, day
      verdamping_monteith, maand, 295482, evaporation_monteith, month
      verdamping_monteith, jaar, 295483, evaporation_monteith, year
      verdamping_penman, 15min, 204341, evaporation_penman, 15min
      verdamping_penman, dag, 295474, evaporation_penman, day
      verdamping_penman, maand, 295475, evaporation_penman, month
      verdamping_penman, jaar, 295479, evaporation_penman, year
      watersnelheid, 15min, 192901, water_velocity, 15min
      watersnelheid, uur, 192902, water_velocity, hour
      watersnelheid, dag, 192903, water_velocity, day
      watersnelheid, maand, 192904, water_velocity, month
      watersnelheid, jaar, 192905, water_velocity, year
      waterstand, 15min, 192780, water_level, 15min
      waterstand, uur, 192785, water_level, hour
      waterstand, dag, 192782, water_level, day
      waterstand, maand, 192783, water_level, month
      waterstand, jaar, 192784, water_level, year
      watertemperatuur, 15min, 325066, water_temperature, 15min
      windrichting, 15min, 192926, wind_direction, 15min
      windspeed, 15min, 192925, wind_speed, 15min

HIC - Cmd timeseriesgroup_ids
-----------------------------

Similar for the VMM, the list of available group identifiers (date: 2023-03-03) are
provided in the following table. `Source <https://hicws.vlaanderen.be/Manual_for_the_use_of_webservices_HIC.pdf>`_

.. Caution:: These identifiers are not described as stable identifiers and can change in time!

.. csv-table:: HIC - Cmd timeseriesgroup_ids
   :header: "group_id", "group_name", "group_type", "stationparameter_longname", "ts_unitname", "ts_unitsymbol"
   :widths: 10, 15, 15, 10, 10, 5

      156158,DL_Stroomrichting,timeseries,Flow Direction,degree,°
      156159,DL_NCatch,timeseries,Catchment Rainfall,millimeter,mm
      156162,DL_H_dag,timeseries,River Stage,meter,m
      156163,DL_H_hr,timeseries,River Stage,meter,m
      156164,DL_H_uur,timeseries,River Stage,meter,m
      156165,DL_HWLW,timeseries,Tidal Water Level,meter,m
      156166,DL_Pluvio_Day_HICOTT,timeseries,Rainfall,millimeter,mm
      156167,DL_Pluvio_Hr_HICOTT,timeseries,Rainfall,millimeter,mm
      156168,DL_Pluvio_uur_HICOTT,timeseries,Rainfall,millimeter,mm
      156169,DL_Q_dag,timeseries,River Discharge,cubic meter per second,m³/s
      156170,DL_Q_hr,timeseries,River Discharge,cubic meter per second,m³/s
      156171,DL_Q_uur,timeseries,River Discharge,cubic meter per second,m³/s
      156172,DL_Chlorofyl,timeseries,Chlorofyl a,microgram per litre,µg/l
      156173,DL_Conductiviteit,timeseries,Conductivity,microsiemens per centimeter,µS/cm
      156188,DL_SSC,timeseries,Suspended Sediment Concentration Calculated,milligram per litre,mg/l
      156190,DL_Pluvio_maand_HICOTT,timeseries,Rainfall,millimeter,mm
      156191,DL_Pluvio_jaar_HICOTT,timeseries,Rainfall,millimeter,mm
      156197,DL_pH,timeseries,pH,scalar,-
      156199,DL_Snelheid_Sediment,timeseries,Flow Velocity,meter per second,m/s
      156200,DL_Temperatuur_Sediment,timeseries,Temperature,degree Celsius,°C
      156202,DL_Turbiditeit,timeseries,Turbidity_NTU,nephlometric turbidity unit,NTU
      156207,DL_Zuurstofgehalte,timeseries,Oxygen Concentration,milligram per litre,mg/l
      156208,DL_Zuurstofverzadiging,timeseries,Oxygen Saturation,percentage,%
      260592,DL_Discharge_calc,timeseries,River Discharge,cubic meter per second,m³/s
      350099,DL_astroHWLW_TAW,timeseries,W_voorspeld,meter,m
      354718,DL_astroContinu_TAW,timeseries,W_voorspeld,meter,m
      421208,DL_Saliniteit,timeseries,Salinity,Practical salinity scale,psu
      510205,DL_HW,timeseries,Tidal Water Level,meter,m
      510207,DL_LW,timeseries,Tidal Water Level,meter,m
      512458,DL_astroContinu_LAT,timeseries,W_voorspeld,decimeter,dm
      515316,DL_astroHWLW_LAT,timeseries,W_voorspeld,decimeter,dm


HIC - Ensemble timeseriesgroup_ids
----------------------------------

The list of available group identifiers for ensemble time series (date: 2023-03-03) are
provided in the following table. `Source <https://hicws.vlaanderen.be/Manual_for_the_use_of_webservices_HIC.pdf>`_

.. Caution:: These identifiers are not described as stable identifiers and can change in time!


.. csv-table:: HIC - Cmd timeseriesgroup_ids
   :header: "group_id", "group_name", "group_type", "stationparameter_longname", "ts_unitname", "ts_unitsymbol"
   :widths: 10, 15, 15, 10, 10, 5

      432821,DL_VerwachtingenHWLW,timeseries,W_voorspeld,meter,m
      506056,DL_PeilVoorspeld_KTdet,timeseries,H_voorspeld,meter,m
      506057,DL_AfvoerVoorspeld_KTdet,timeseries,Q_voorspeld,cubic meter per second,m³/s
      506058,DL_PeilVoorspeld_LTdet,timeseries,H_voorspeld,meter,m
      506059,DL_AfvoerVoorspeld_LTdet,timeseries,Q_voorspeld,cubic meter per second,m³/s
      506060,DL_NCatch_KTdet,timeseries,Ncatch_voorspeld,millimeter,mm
      506061,DL_NCatch_LTdet,timeseries,Ncatch_voorspeld,millimeter,mm
