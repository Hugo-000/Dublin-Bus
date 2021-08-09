from django.test import TestCase
from scrapper.models import CurrentWeather, ForecastWeather, Routes, Stops, AllStopsWithRoute, Covid, RoutePrediction
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("test base", BASE_DIR)
# creating dummy model instances
class ModelTest(TestCase):
    @classmethod
    def setUp(cls):
        CurrentWeather.objects.create(
            dt="01-01-2021",
            temp="10",
            feels_like="10",
            temp_min="10",
            temp_max="10",
            pressure="10",
            humidity="5",
            wind_speed="2",
            wind_deg="2",
            clouds_all="1",
            weather_main="test",
            weather_description="test",
            weather_icon="01n"
        )

        ForecastWeather.objects.create(
            dt="2021-01-01",
            dt_iso="10",
            temp="10",
            feels_like="10",
            temp_min="10",
            temp_max="10",
            pressure="10",
            humidity="10",
            wind_speed="10",
            wind_deg="10",
            clouds_all="10",
            weather_id="10",
            weather_main="10",
            weather_description="test",
            weather_icon="01n",
            rain_1h="0",
            weekday="1",
            month="1",
        )

        Covid.objects.create(
            dt="1",
            icu="0",
            totalConfirmedCases="0",
            totalDeaths="0",
            confirmedCases="0",
            confirmedDeaths="0",
            statisticsProfileDt="0",
            fid="0",
            hospitalisedCases="0",
        )

        Routes.objects.create(
            route_name="test",
            route_description="test",
            route_direction="test"
        )

        Stops.objects.create(
            stop_id="8220DB000004",
            stop_name="test",
            lat="10",
            lng="10",
            stop_number="2"
        )
        RoutePrediction.objects.create(
            Route="33E",
            Direction="I",
            StopOrder="1",
            StopID="2",
            PercentDone="3",
            ID="1"
        )

    def test_CurrentWeather_data(self):
        data = CurrentWeather.objects.get(dt="01-01-2021")
        expected_data = (
                f"{data.dt},"
                f"{data.temp},"
                f"{data.feels_like},"
                f"{data.temp_min},"
                f"{data.temp_max},"
                f"{data.pressure},"
                f"{data.humidity},"
                f"{data.wind_speed},"
                f"{data.wind_deg},"
                f"{data.clouds_all},"
                f"{data.weather_main},"
                f"{data.weather_description},"
                f"{data.weather_icon},"
            )
        print("<<<<<<<<Verifying Model Current Weather>>>>>>")
        self.assertEquals(expected_data, str(data))

    def test_Forecastweather_data(self):
        data = ForecastWeather.objects.get(dt="2021-01-01")
        expected_data = (
            f"{data.dt},"
            f"{data.dt_iso},"
            f"{data.temp},"
            f"{data.feels_like},"
            f"{data.temp_min},"
            f"{data.temp_max},"
            f"{data.pressure},"
            f"{data.humidity},"
            f"{data.wind_speed},"
            f"{data.wind_deg},"
            f"{data.clouds_all},"
            f"{data.weather_id},"
            f"{data.weather_main},"
            f"{data.weather_description},"
            f"{data.weather_icon},"
            f"{data.rain_1h},"
            f"{data.weekday},"
            f"{data.month},"
        )
        print("<<<<<<<<Verifying Model Forcast Weather>>>>>>")
        self.assertEquals(expected_data, str(data))

    def test_Covid_data(self):
        data = Covid.objects.get(dt="1")
        print("<<<<<<<<Verifying Covid Model>>>>>>")
        self.assertIsNotNone(data)

    def test_Routes(self):
        data = Routes.objects.get(route_name="test")
        print("<<<<<<<<Verifying Routes Model>>>>>>")
        self.assertIsNotNone(data)
    def test_Stops(self):
        data = Stops.objects.get(stop_id="8220DB000004")
        print("<<<<<<<<Verifying Stops Model>>>>>>")
        self.assertIsNotNone(data)

