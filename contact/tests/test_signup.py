import datetime
import time

from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class SignUpTest(LiveServerTestCase):
    
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(SignUpTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SignUpTest, self).tearDown()

    def fill_registration_form(self, values):
        username = self.selenium.find_element_by_name('username')
        email = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        username.send_keys(values['username'])
        email.send_keys(values['email'])
        password.send_keys(values['password'])
        self.selenium.find_element_by_id("userform").submit()

    def test_null_values(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': '', 'email': '', 'password': ''}
        self.fill_registration_form(values)
        self.assertEqual(len(User.objects.all()), 0)

    def test_successful_registration(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': 'testuser', 'email': 'testuser@test.com', 'password': 'testpass'}
        self.fill_registration_form(values)
        self.assertEqual(self.selenium.current_url, self.live_server_url+'/login/')
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_username(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': 'testuser', 'email': 'testuser@test.com', 'password': 'testpass'}
        self.fill_registration_form(values)
        self.assertEqual(self.selenium.current_url, self.live_server_url+'/login/')
        self.assertEqual(len(User.objects.all()), 1)
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': 'testuser', 'email': 'testuser1@test.com', 'password': 'testpass'}
        self.fill_registration_form(values)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicate_email(self):
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': 'testuser', 'email': 'testuser@test.com', 'password': 'testpass'}
        self.fill_registration_form(values)
        self.assertEqual(self.selenium.current_url, self.live_server_url+'/login/')
        self.assertEqual(len(User.objects.all()), 1)
        self.selenium.get('%s%s' % (self.live_server_url,  "/register/"))
        values = {'username': 'testuser1', 'email': 'testuser@test.com', 'password': 'testpass'}
        self.fill_registration_form(values)
        self.assertEqual(len(User.objects.all()), 1)