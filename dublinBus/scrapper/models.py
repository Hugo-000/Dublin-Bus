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


