import time

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class GuiTestWithSelenium(TestCase):

    def test_home_page_firefox(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Vítej v našem houbovém světě!' in selenium_webdriver.page_source

    def test_home_page_chrome(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Vítej v našem houbovém světě!' in selenium_webdriver.page_source

    def test_signup(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/accounts/registration/')
        time.sleep(0.3)
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(0.3)
        first_name_field = selenium_webdriver.find_element(By.ID, 'id_first_name')
        first_name_field.send_keys('Name')
        time.sleep(0.3)
        last_name_field = selenium_webdriver.find_element(By.ID, 'id_last_name')
        last_name_field.send_keys('Surname')
        time.sleep(0.3)
        password1_field = selenium_webdriver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('SDdskj45!dfa@')
        time.sleep(0.3)
        password2_field = selenium_webdriver.find_element(By.ID, 'id_password2')
        password2_field.send_keys('SDdskj45!dfa@')
        time.sleep(0.3)
        biography_field = selenium_webdriver.find_element(By.ID, 'id_biography')
        biography_field.send_keys('Nějaký text.')
        time.sleep(0.3)
        submit_button = selenium_webdriver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(3)

        # assert 'Welcome to our Hollymovie' in selenium_webdriver.page_source
        assert 'A user with that username already exists.' in selenium_webdriver.page_source