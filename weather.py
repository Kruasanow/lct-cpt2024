import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def get_weather(past_days, forecast_days, latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "forecast_days": forecast_days,
        "past_days": past_days,
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
                   "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth",
                   "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low",
                   "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration",
                   "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m",
                   "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m",
                   "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m",
                   "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm",
                   "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm",
                   "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm", "uv_index",
                   "uv_index_clear_sky", "is_day", "cape", "freezing_level_height", "sunshine_duration",
                   "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance",
                   "global_tilted_irradiance", "terrestrial_radiation", "shortwave_radiation_instant",
                   "direct_radiation_instant", "diffuse_radiation_instant", "direct_normal_irradiance_instant",
                   "global_tilted_irradiance_instant", "terrestrial_radiation_instant"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
    hourly_rain = hourly.Variables(6).ValuesAsNumpy()
    hourly_showers = hourly.Variables(7).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(12).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
    hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
    hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
    hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
    hourly_wind_direction_120m = hourly.Variables(27).ValuesAsNumpy()
    hourly_wind_direction_180m = hourly.Variables(28).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
    hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
    hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
    hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
    hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
    hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
    hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
    hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
    hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
    hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
    hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
    hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
    hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(42).ValuesAsNumpy()
    hourly_uv_index_clear_sky = hourly.Variables(43).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(44).ValuesAsNumpy()
    hourly_cape = hourly.Variables(45).ValuesAsNumpy()
    hourly_freezing_level_height = hourly.Variables(46).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(47).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(48).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(49).ValuesAsNumpy()
    hourly_diffuse_radiation = hourly.Variables(50).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(51).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(52).ValuesAsNumpy()
    hourly_terrestrial_radiation = hourly.Variables(53).ValuesAsNumpy()
    hourly_shortwave_radiation_instant = hourly.Variables(54).ValuesAsNumpy()
    hourly_direct_radiation_instant = hourly.Variables(55).ValuesAsNumpy()
    hourly_diffuse_radiation_instant = hourly.Variables(56).ValuesAsNumpy()
    hourly_direct_normal_irradiance_instant = hourly.Variables(57).ValuesAsNumpy()
    hourly_global_tilted_irradiance_instant = hourly.Variables(58).ValuesAsNumpy()
    hourly_terrestrial_radiation_instant = hourly.Variables(59).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature_2m": hourly_temperature_2m, "relative_humidity_2m": hourly_relative_humidity_2m,
        "dew_point_2m": hourly_dew_point_2m, "apparent_temperature": hourly_apparent_temperature,
        "precipitation_probability": hourly_precipitation_probability, "precipitation": hourly_precipitation,
        "rain": hourly_rain, "showers": hourly_showers, "snowfall": hourly_snowfall, "snow_depth": hourly_snow_depth,
        "weather_code": hourly_weather_code, "pressure_msl": hourly_pressure_msl,
        "surface_pressure": hourly_surface_pressure, "cloud_cover": hourly_cloud_cover,
        "cloud_cover_low": hourly_cloud_cover_low, "cloud_cover_mid": hourly_cloud_cover_mid,
        "cloud_cover_high": hourly_cloud_cover_high, "visibility": hourly_visibility,
        "evapotranspiration": hourly_evapotranspiration,
        "et0_fao_evapotranspiration": hourly_et0_fao_evapotranspiration,
        "vapour_pressure_deficit": hourly_vapour_pressure_deficit, "wind_speed_10m": hourly_wind_speed_10m,
        "wind_speed_80m": hourly_wind_speed_80m, "wind_speed_120m": hourly_wind_speed_120m,
        "wind_speed_180m": hourly_wind_speed_180m, "wind_direction_10m": hourly_wind_direction_10m,
        "wind_direction_80m": hourly_wind_direction_80m, "wind_direction_120m": hourly_wind_direction_120m,
        "wind_direction_180m": hourly_wind_direction_180m, "wind_gusts_10m": hourly_wind_gusts_10m,
        "temperature_80m": hourly_temperature_80m, "temperature_120m": hourly_temperature_120m,
        "temperature_180m": hourly_temperature_180m, "soil_temperature_0cm": hourly_soil_temperature_0cm,
        "soil_temperature_6cm": hourly_soil_temperature_6cm, "soil_temperature_18cm": hourly_soil_temperature_18cm,
        "soil_temperature_54cm": hourly_soil_temperature_54cm, "soil_moisture_0_to_1cm": hourly_soil_moisture_0_to_1cm,
        "soil_moisture_1_to_3cm": hourly_soil_moisture_1_to_3cm,
        "soil_moisture_3_to_9cm": hourly_soil_moisture_3_to_9cm,
        "soil_moisture_9_to_27cm": hourly_soil_moisture_9_to_27cm,
        "soil_moisture_27_to_81cm": hourly_soil_moisture_27_to_81cm, "uv_index": hourly_uv_index,
        "uv_index_clear_sky": hourly_uv_index_clear_sky, "is_day": hourly_is_day, "cape": hourly_cape,
        "freezing_level_height": hourly_freezing_level_height, "sunshine_duration": hourly_sunshine_duration,
        "shortwave_radiation": hourly_shortwave_radiation, "direct_radiation": hourly_direct_radiation,
        "diffuse_radiation": hourly_diffuse_radiation, "direct_normal_irradiance": hourly_direct_normal_irradiance,
        "global_tilted_irradiance": hourly_global_tilted_irradiance,
        "terrestrial_radiation": hourly_terrestrial_radiation,
        "shortwave_radiation_instant": hourly_shortwave_radiation_instant,
        "direct_radiation_instant": hourly_direct_radiation_instant,
        "diffuse_radiation_instant": hourly_diffuse_radiation_instant,
        "direct_normal_irradiance_instant": hourly_direct_normal_irradiance_instant,
        "global_tilted_irradiance_instant": hourly_global_tilted_irradiance_instant,
        "terrestrial_radiation_instant": hourly_terrestrial_radiation_instant}

    return pd.DataFrame(data=hourly_data), response.Latitude(), response.Longitude(), response.Elevation()