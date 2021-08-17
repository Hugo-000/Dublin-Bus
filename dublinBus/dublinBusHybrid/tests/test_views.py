from django.test import TestCase
from django.urls import resolve
from dublinBusHybrid.views import JourneyPlanner, BusRoutes, Index
from dublinBusHybrid.forms import JourneyPlannerForm
import datetime
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("test base", BASE_DIR)


class TestIndexView(TestCase):
    def test_resolve_to_index(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/dublinBusHybrid/')

        # check function name is equal
        self.assertEqual(found.func.__name__, Index.as_view().__name__)

    def test_resolve_to_test_get_jounrney_planner_page(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/dublinBusHybrid/journeyPlanner/')

        # check function name is equal
        self.assertEqual(found.func.__name__, JourneyPlanner.as_view().__name__)

    def test_resolve_to_test_get_route_page(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/dublinBusHybrid/Routes/')

        # check function name is equal
        self.assertEqual(found.func.__name__, BusRoutes.as_view().__name__)

    def test_get_journey_planner_page_response(self):
        """test the get method"""
        # get url localhost:8000/
        response = self.client.get('/dublinBusHybrid/journeyPlanner/')

        # check which template is used
        self.assertTemplateUsed(response, 'journeyPlanner.html')

        # check response status is equal to 200
        self.assertEqual(response.status_code, 200)

    def test_get_directions(self):
        """test if the direction can e inferenced by lat and lng data: "UCD","UCD","2021-08-06","16:00"""
        response = self.client.post("/dublinBusHybrid/journeyPlanner/",
                                    {'origin_location': 'UCD', 'destination_location': 'Rathmines',
                                     'travel_date': '2021-08-08', 'travel_time': '16:00'},
                                    HTTP_ACCEPT='application/json')
        # # content_type  = "application/json"
        # print(response.content)
        # print(response.status_code)
        # direction = JourneyPlanner().fetchJSON("UCD")
        self.assertEqual(response.status_code, 200)

    def test_get_route_by_number(self):
        """test if stops sequence of a route can be retrieved by route number"""
        response = self.client.post("/dublinBusHybrid/Routes/", {'route_name': '66E,0'})
        # CurrentWeather.objects.get(dt="01-01-2021")
        # response = self.client.resolve("/dublinBusHybrid/Routes/", {'route_name': '66E', 'direction': '0'})
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes.html')
        # self.assertEqual(len(response.context['route']), 1)

    def test_get_route_by_number_404(self):
        """test if stops sequence of a route can be retrieved by route number"""
        response = self.client.post("/dublinBusHybrid/Routes/", {'route_name': '44324, I'})
        with self.assertRaises(IndexError):
            #response.content['route_Info']
            self.assertEqual(response.status_code, 200)
            self.assertRaises(IndexError, response)

    def test_jouurney_planner(self):
        """test data from the post method can successfully predict the query without transfer"""
        request = {'user':{'Error': 'User is not authenticated'},
                    'travel_date': datetime.date(2021, 8, 12),
                   'travel_time': datetime.time(21, 0),
                   'Steps': [{
                       'distance': {
                           'text': '54 m',
                           'value': 54
                       },
                       'duration': {
                           'text': '1 min',
                           'value': 38
                       },
                       'Instructions': 'Walk to Coolock Drive, stop 1249',
                       'travel_mode': 'WALKING'
                   },
                       {
                           'distance': {
                               'text': '8.2 km',
                               'value': 8234
                           },
                           'duration': {
                               'text': '26 mins',
                               'value': 1561
                           },
                           'instructions': 'Bus towards Jobstown',
                           'transit': {
                               'arrival_stop': {
                                   'location': {
                                       'lat': 53.3441118,
                                       'lng': -6.265506299999999
                                   },
                                   'name': 'Dame Street, stop 1934'
                               },
                               'arrival_time': {
                                   'text': '21:27',
                                   'time_zone': 'Europe/Dublin',
                                   'value': '2021-08-12T20:27:10.000Z'
                               },
                               'departure_stop': {
                                   'location': {
                                       'lat': 53.395181,
                                       'lng': -6.2012402
                                   },
                                   'name': 'Coolock Drive, stop 1249'
                               },
                               'departure_time': {
                                   'text': '21:01',
                                   'time_zone': 'Europe/Dublin',
                                   'value': '2021-08-12T20:01:09.000Z'
                               },
                               'headsign': 'Jobstown',
                               'line': {
                                   'agencies': [{
                                       'name': 'Dublin Bus',
                                       'url': 'https://www.dublinbus.ie/'
                                   }],
                                   'color': '#f2ca36',
                                   'name': 'Templeview Avenue - Fortunestown Road',
                                   'short_name': '27',
                                   'text_color': '#000000',
                                   'vehicle': {
                                       'icon': 'https://maps.gstatic.com/mapfiles/transit/iw2/6/bus2.png',
                                       'name': 'Bus', 'type': 'BUS'
                                   }
                               },
                               'num_stops': 27
                           },
                           'travel_mode': 'TRANSIT'
                       },
                       {
                           'distance': {
                               'text': '46 m',
                               'value': 46
                           },
                           'duration': {
                               'text': '1 min',
                               'value': 35
                           },
                           'instructions': 'Walk to Dame St, Dublin, Ireland',
                           'travel_mode': 'WALKING'
                       }]
                   }
        j = JourneyPlanner()
        prediction =j.post(request=request,user={'Error': 'User is not authenticated'})
        self.assertTrue(isinstance(prediction, int))

