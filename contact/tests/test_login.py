import datetime
import time

from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(LiveServerTestCase):
    
    def setUp(self):
    	User.objects.create_superuser(
            username='testuser',
            password='testpass',
            email='testuser@test.com'
        )

        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(LoginTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LoginTest, self).tearDown()

    def fill_login_form(self, values):
        username = self.selenium.find_element_by_name('username')
        password = self.selenium.find_element_by_name('password')
        username.send_keys(values['username'])
        password.send_keys(values['password'])
        self.selenium.find_element_by_id("loginform").submit()

    def test_invalid_credentials(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/login/"))
        values = {'username': 'testuser', 'password': 'wrongtestpass'}
        self.fill_login_form(values)
        self.assertEqual(self.selenium.current_url, self.live_server_url+'/login/')
        self.assertNotEqual(self.selenium.current_url, self.live_server_url+'/contact/list/')

    def test_valid_credentials(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/login/"))
        values = {'username': 'testuser', 'password': 'testpass'}
        self.fill_login_form(values)
        self.assertNotEqual(self.selenium.current_url, self.live_server_url+'/login/')
        self.assertEqual(self.selenium.current_url, self.live_server_url+'/contact/list/')
  