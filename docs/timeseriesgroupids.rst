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

HIC
---

Similar for the HIC, the list of available group identifiers (date: 2019-09-17) are provided
in the following table.

.. Caution:: These identifiers are not described as stable identifiers and can change in time!

.. csv-table:: HIC published timeseriesgroup identifiers
   :header: "variable (nl)", "frequency_nl", "timeseriesgroup_id", "variable (en)", "frequency (en)"
   :widths: 10, 5, 10, 10, 5

      afvoer, hoge resolutie, 156170, discharge, high resolution
      afvoer, uur, 156171, discharge, hour
      afvoer, dag, 156169, discharge, day
      astronomische voorspellingen hoog-en laagwaters tijgebied Schelde, , 350099, astronomical predictions high-and low water tidal area Schelde,
      astronomische voorspellingen continu reeksen tijgebied Schelde, , 354718, astronomical predictions continuous time series tidal area Schelde,
      berekende bovenafvoer Zeeschelde thv Schelle, , 260592, calculated discharge Zeeschelde at Schelle,
      chlorofyl, hoge resolutie, 156172, chlorofyl, high resolution
      conductiviteit, hoge resolutie, 156173, conductivity, high resolution
      gebiedsneerslagen belangrijke meetlocaties HIC (gemeten en voorspeld), ,156159, area rainfall main locations HIC (measured and predicted),
      neerslag, hoge resolutie, 156167, rainfall, high resolution
      neerslag, uur, 156168, rainfall, hour
      neerslag, dag, 156166, rainfall, day
      neerslag, maand, 156190, rainfall, month
      neerslag, jaar, 156191, rainfall, year
      saliniteit, hoge resolutie, 421208, salinity, high resolution
      sediment concentratie, hoge resolutie, 156188, sediment concentration, high resolution
      stroomrichting, hoge resolutie, 156158, flow direction, high resolution
      stroomsnelheid, hoge resolutie, 156199, flow speed, high resolution
      turbiditeit, hoge resolutie, 156202, turbidity, high resolution
      waterstand, hoge resolutie, 156163, water level, high resolution
      waterstand, uur, 156164, water level, hour
      waterstand, dag, 156162, water level, day
      waterstand hoog-en laagwaters tijgebied Schelde, ,156165, water level high-and low water tidal area Schelde
      watertemperatuur, hoge resolutie, 156200, water temperature, high resolution
      zuurstofgehalte, hoge resolutie, 156207, oxygen concentration, high resolution
      zuurstofverzadiging, hoge resolutie, 456208, oxygen saturation, high resolution
      zuurtegraad, hoge resolutie, 156197, acidity, high resolution
