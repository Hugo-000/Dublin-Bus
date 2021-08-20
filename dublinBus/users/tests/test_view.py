from django.test import TestCase
from django.urls import resolve
from users.views import Dashboard
import os
import sys
from django.contrib.auth import views as auth_views

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("test base", BASE_DIR)

class TestUser(TestCase):
    def test_correct_template_used(self):
        """test login_template_is_correctly_used"""
        # resolve root path
        found = self.client.get('/accounts/login/')
        # check the correct template is rendered
        self.assertTemplateUsed(found, 'registration/login.html')

    def test_resolve_to_is_login(self):
        """test login_url works fine"""
        # resolve login path
        found = resolve('/accounts/login/')
        self.assertEqual(found.func.__name__, auth_views.LoginView.as_view( ).__name__)
        # check the correct template is rendered
        #self.assertTemplateUsed(found, 'login.html')

    def test_login_with_correct_user(self):
        """test user can login with correct user name and password"""
        # resolve root path
        response = self.client.post('/accounts/login/', {'username':'Jen', 'password':'DublinBus1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, auth_views.LoginView.as_view( ).__name__)

    def test_login_with_incorrect_user_password(self):
        """test user can login with incorrect_user_password"""
        response = self.client.post('/accounts/login/', {'username':'Jen', 'password':'ABC'}, follow=True)
        print(response.status_code)

    def test_login_with_incorrect_username(self):
        """test user can login with incorrect_username"""
        response = self.client.post('/accounts/login/', {'username':'Jenn', 'password':'ABC'}, follow=True)
        print(response.context)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)







