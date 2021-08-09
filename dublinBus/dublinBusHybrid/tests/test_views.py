from django.test import TestCase
from django.urls import resolve
from dublinBusHybrid.views import JourneyPlanner, BusRoutes, Index
from dublinBusHybrid.forms import JourneyPlannerForm
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
        self.assertEqual(found.func.__name__, JourneyPlanner.as_view( ).__name__)

    def test_resolve_to_test_get_route_page(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/dublinBusHybrid/Routes/')

        # check function name is equal
        self.assertEqual(found.func.__name__, BusRoutes.as_view( ).__name__)

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
        response = self.client.post("/dublinBusHybrid/journeyPlanner/", {'origin_location': 'UCD', 'destination_location': 'Rathmines','travel_date':'2021-08-08','travel_time':'16:00'},
                                    HTTP_ACCEPT='application/json')
        # # content_type  = "application/json"
        #print(response.content)
        # print(response.status_code)
        #direction = JourneyPlanner().fetchJSON("UCD")
        self.assertEqual(response.status_code, 200)

    def test_get_route_by_number(self):
        """test if stops sequence of a route can be retrieved by route number"""
        response = self.client.post("/dublinBusHybrid/Routes/", {'route_name': '66E,0'})
        #CurrentWeather.objects.get(dt="01-01-2021")
        #response = self.client.resolve("/dublinBusHybrid/Routes/", {'route_name': '66E', 'direction': '0'})
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes.html')
        #self.assertEqual(len(response.context['route']), 1)

    def test_get_route_by_number_404(self):
        """test if stops sequence of a route can be retrieved by route number"""
        response = self.client.post("/dublinBusHybrid/Routes/", {'route_name': '44324'})
        with self.assertRaises(IndexError):
            response.content['route_Info']
            self.assertEqual(response.status_code, 404)
            self.assertRaises(IndexError, response)


