from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CurrentWeather(models.Model):
    dt = models.CharField(max_length=45, primary_key=True)
    temp = models.CharField(max_length=10, null=True)
    feels_like = models.CharField(max_length=45, null=True)
    temp_min = models.CharField(max_length=45, null=True)
    temp_max = models.CharField(max_length=45, null=True)
    pressure = models.CharField(max_length=45, null=True)
    humidity = models.CharField(max_length=45, null=True)
    wind_speed = models.CharField(max_length=45, null=True)
    wind_deg = models.CharField(max_length=45, null=True)
    clouds_all = models.CharField(max_length=45, null=True)
    weather_main = models.CharField(max_length=45, null=True)
    weather_description = models.CharField(max_length=45, null=True)
    weather_icon = models.CharField(max_length=45, null=True)

    def __str__(self):
        result = (
            f"{self.dt},"
            f"{self.temp},"
            f"{self.feels_like},"
            f"{self.temp_min},"
            f"{self.temp_max},"
            f"{self.pressure},"
            f"{self.humidity},"
            f"{self.wind_speed},"
            f"{self.wind_deg},"
            f"{self.clouds_all},"
            f"{self.weather_main},"
            f"{self.weather_description},"
            f"{self.weather_icon},"
        )
        return result

class ForecastWeather(models.Model):
    dt = models.CharField(max_length=45, primary_key=True)
    dt_iso = models.CharField(max_length=45, null=True)
    temp = models.CharField(max_length=45, null=True)
    feels_like = models.CharField(max_length=45, null=True)
    temp_min = models.CharField(max_length=45, null=True)
    temp_max = models.CharField(max_length=45, null=True)
    pressure = models.CharField(max_length=45, null=True)
    humidity = models.CharField(max_length=45, null=True)
    wind_speed = models.CharField(max_length=45, null=True)
    wind_deg = models.CharField(max_length=45, null=True)
    clouds_all = models.CharField(max_length=45, null=True)
    weather_id = models.CharField(max_length=45, null=True)
    weather_main = models.CharField(max_length=45, null=True)
    weather_description = models.CharField(max_length=45, null=True)
    weather_icon = models.CharField(max_length=45, null=True)
    rain_1h = models.CharField(max_length=45, default="0", null=True)
    weekday = models.CharField(max_length=10, null=True)
    month = models.CharField(max_length=10, null=True)

    def __str__(self):
        result = (
            f"{self.dt}",
            f"{self.dt_iso}",
            f"{self.temp}",
            f"{self.temp_min}",
            f"{self.temp_max}",
            f"{self.pressure}",
            f"{self.humidity}",
            f"{self.wind_speed}",
            f"{self.wind_deg}",
            f"{self.clouds_all}",
            f"{self.weather_id}",
            f"{self.weather_main}",
            f"{self.weather_description}",
            f"{self.weather_icon}",
        )
        return result
class Routes(models.Model):
    route_id = models.CharField(max_length=45, null=True)
    agency_id = models.CharField(max_length=45, null=True)
    route_name = models.CharField(max_length=45, null=True)
    route_description = models.CharField(max_length=200, null=True)
    route_direction = models.CharField(max_length=45, null=True)


class Stops(models.Model):
    stop_id = models.CharField(max_length=20, primary_key=True)
    stop_name = models.CharField(max_length=45, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    stop_number = models.CharField(max_length=45, null=True)

class AllStopsWithRoute(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    stop_sequence = models.CharField(max_length=45, null=True)
    stop_headsign = models.CharField(max_length=45, null=True)
    route_number = models.CharField(max_length=45, null=True)
    stop = models.ForeignKey(Stops, on_delete=models.SET_NULL, null=True)
    direction = models.CharField(max_length=10, null=True)
    subRoute = models.CharField(max_length=10, null=True)

class Covid(models.Model):
    dt = models.CharField(max_length=45, primary_key=True)
    icu = models.CharField(max_length=45, default="0", null=True)
    totalConfirmedCases = models.CharField(max_length=45, default="0", null=True)
    totalDeaths = models.CharField(max_length=45, default="0", null=True)
    confirmedCases = models.CharField(max_length=45, default="0", null=True)
    confirmedDeaths = models.CharField(max_length=45, default="0",null=True)
    statisticsProfileDt = models.CharField(max_length=45, default="0", null=True)
    fid = models.CharField(max_length=45, default="0", null=False)
    hospitalisedCases = models.CharField(max_length=45,default="0", null=True)

class RoutePrediction(models.Model):
    Route = models.CharField(max_length=10, null=True)
    Direction = models.CharField(max_length=10, null=True)
    StopOrder = models.CharField(max_length=10, null=True)
    StopID = models.CharField(max_length=10, null=True)
    PercentDone = models.CharField(max_length=10, null=True)
    ID = models.CharField(max_length=45, primary_key=True)

class RealTimeTraffic(models.Model):
    route_number = models.CharField(max_length=45, null=True)
    direction = models.CharField(max_length=45, null=True)
    start_time = models.CharField(max_length=45, null=True)
    start_date = models.CharField(max_length=45, null=True)
    trip_schedule = models.CharField(max_length=45, null=True)
    stop_departure_delay = models.CharField(max_length=45, default="na", null=True)
    stop_arrival_delay = models.CharField(max_length=45, default="na", null=True)
    stop_id = models.CharField(max_length=45, null=True)
    stop_schedule = models.CharField(max_length=45, null=True)
class Agency(models.Model):
    agency_id = models.CharField(max_length=45, null=True)
    agency_name = models.CharField(max_length=45, null=True)
    agency_url = models.CharField(max_length=45, null=True)
    agency_timezone = models.CharField(max_length=45, null=True)
    agency_lang = models.CharField(max_length=45, null=True)

class StopTimes(models.Model):
    trip_id = models.CharField(max_length=45, null=True)
    arrival_time = models.CharField(max_length=45, null=True)
    departure_time = models.CharField(max_length=45, null=True)
    stop_id = models.CharField(max_length=45, null=True)
    stop_sequence = models.CharField(max_length=45, null=True)
    stop_headsign = models.CharField(max_length=45, null=True)
    pickup_type = models.CharField(max_length=45, null=True)
    drop_off_type = models.CharField(max_length=45, null=True)
    shape_dist_traveled = models.CharField(max_length=45, null=True) 

class StopTimes2(models.Model):
    trip_id = models.CharField(max_length=45, null=True)
    arrival_time = models.CharField(max_length=45, null=True)
    departure_time = models.CharField(max_length=45, null=True)
    stop_id = models.CharField(max_length=45, null=True)
    stop_sequence = models.CharField(max_length=45, null=True)
    stop_headsign = models.CharField(max_length=45, null=True)
    pickup_type = models.CharField(max_length=45, null=True)
    drop_off_type = models.CharField(max_length=45, null=True)
    shape_dist_traveled = models.CharField(max_length=45, null=True) 

class Trips(models.Model):
    route_id = models.CharField(max_length=45, null=True)
    service_id = models.CharField(max_length=45, null=True)
    trip_id = models.CharField(max_length=45, null=True)
    shape_id = models.CharField(max_length=45, null=True)
    trip_headsign = models.CharField(max_length=100, null=True)
    direction_id = models.CharField(max_length=45, null=True)

