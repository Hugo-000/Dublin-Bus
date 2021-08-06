from django.test import TestCase
from django.urls import resolve
from dublinBusHybrid.views import JourneyPlanner
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("test base", BASE_DIR)

from django.test.runner import DiscoverRunner


# myapp.tests.py
from django.test import TestCase, SimpleTestCase


class DbTestCase(TestCase):
    """Does something with the DB."""
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass



class NoDbTestCase(SimpleTestCase):
    """Does something with the DB."""
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass

class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation/deletion """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass



class TestIndexView(TestCase):

    def test_resolve_to_test_get_index(self):
        """test the url works fine"""
        # resolve root path
        found = resolve('/')

        # check function name is equal
        self.assertEqual(found.func.__name__, JourneyPlanner.as_view( ).__name__)


