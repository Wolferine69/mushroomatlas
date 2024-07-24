import time
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

class GuiTestWithSelenium(TestCase):
    """
    GUI tests for the Mushroomatlas project using Selenium.

    This test case class contains tests for various features of the Mushroomatlas web application.
    It uses Selenium WebDriver to automate browser actions and validate the application behavior.
    """

    def test_home_page_firefox(self):
        """
        Test the home page using Firefox.

        This test verifies that the home page is correctly displayed using Firefox.
        """
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Vítej v našem houbovém světě!' in selenium_webdriver.page_source

    def test_home_page_chrome(self):
        """
        Test the home page using Chrome.

        This test verifies that the home page is correctly displayed using Chrome.
        """
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Vítej v našem houbovém světě!' in selenium_webdriver.page_source

    def test_signup(self):
        """
        Test the signup process.

        This test automates the signup process and verifies that an error message
        is displayed if the username already exists.
        """
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

        assert 'A user with that username already exists.' in selenium_webdriver.page_source

    def test_login(self):
        """
        Test the login process.

        This test automates the login process and verifies that the user is successfully logged in.
        """
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/accounts/login/')
        time.sleep(0.3)
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(0.3)
        password_field = selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys('SDdskj45!dfa@')
        time.sleep(0.3)
        submit_button = selenium_webdriver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(3)
        assert 'Vítej v našem houbovém světě!' in selenium_webdriver.page_source

    def test_mushroom(self):
        """
        Test the mushroom detail page.

        This test verifies that the mushroom detail page for mushroom with ID 1 is correctly displayed.
        """
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/mushrooms/1/')
        time.sleep(3)
        assert 'Hřib smrkový' in selenium_webdriver.page_source

    # def test_finding(self): #TODO: findings does't response
    #     selenium_webdriver = webdriver.Firefox()
    #     selenium_webdriver.get('http://127.0.0.1:8000/findings/1/')
    #     time.sleep(3)
    #     assert 'Hřib smrkový' in selenium_webdriver.page_source
