import time
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GuiTestWithSelenium(TestCase):
    """
    GUI tests for the Mushroomatlas project using Selenium.

    This test case class contains tests for various features of the Mushroomatlas web application.
    It uses Selenium WebDriver to automate browser actions and validate the application behavior.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the Selenium WebDriver with Firefox.
        """
        self.selenium_webdriver = webdriver.Firefox()

    def login(self):
        """
        Log in to the application.

        This method navigates to the login page, enters the credentials, and submits the form.
        """
        self.selenium_webdriver.get('http://127.0.0.1:8000/accounts/login/')
        time.sleep(0.3)
        username_field = self.selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('FungiFreak')
        time.sleep(0.3)
        password_field = self.selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys('FunGuy123!')
        time.sleep(0.3)
        submit_button = self.selenium_webdriver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(3)

        # Verify login was successful
        assert 'Vítej v našem houbovém světě!' in self.selenium_webdriver.page_source

    def tearDown(self):
        """
        Tear down the test environment.

        This method quits the Selenium WebDriver.
        """
        self.selenium_webdriver.quit()

    def test_recipes(self):
        """
        Test the recipes page.

        This test verifies that the recipe with ID 8 is correctly displayed on the recipes page.
        """
        self.selenium_webdriver.get('http://127.0.0.1:8000/recipes/8/')
        time.sleep(3)
        assert 'Babiččina rychlá kulajda' in self.selenium_webdriver.page_source

    def test_families(self):
        """
        Test the families page.

        This test verifies that the family with ID 3 is correctly displayed on the families page.
        """
        self.selenium_webdriver.get('http://127.0.0.1:8000/families/3/')
        time.sleep(3)
        assert 'Chorošotvaré' in self.selenium_webdriver.page_source

    def test_tip(self):
        """
        Test the tip page.

        This test verifies that the tip with ID 1 is correctly displayed on the tip page.
        """
        self.selenium_webdriver.get('http://127.0.0.1:8000/tip/1/')
        time.sleep(3)
        assert 'Co si vzít na houby?' in self.selenium_webdriver.page_source

    def test_profiles(self):
        """
        Test the profiles page.

        This test verifies that the profile list is correctly displayed after logging in.
        """
        self.login()  # Ensure the user is logged in
        self.selenium_webdriver.get('http://127.0.0.1:8000/accounts/profiles')
        time.sleep(3)
        assert 'ForestExplorer' in self.selenium_webdriver.page_source

    def test_findings_map_firefox(self):
        """
        Test the findings map page with Firefox.

        This test verifies that the findings map is correctly displayed using Firefox.
        """
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/findings_map/')
        time.sleep(5)
        assert 'Nálezy hub' in selenium_webdriver.page_source
        assert selenium_webdriver.find_element(By.ID, 'map') is not None
        assert selenium_webdriver.find_element(By.ID, 'details') is not None
        selenium_webdriver.quit()

    def test_findings_map_chrome(self):
        """
        Test the findings map page with Chrome.

        This test verifies that the findings map is correctly displayed using Chrome.
        """
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/findings_map/')
        time.sleep(5)
        assert 'Nálezy hub' in selenium_webdriver.page_source
        assert selenium_webdriver.find_element(By.ID, 'map') is not None
        assert selenium_webdriver.find_element(By.ID, 'details') is not None
        selenium_webdriver.quit()
