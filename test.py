import os
from unittest import skipIf
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@skipIf(getattr(settings,'SKIP_SELENIUM_TESTS', False), "Skipping Selenium tests\n")
class SeleniumTestCase(LiveServerTestCase):
    user_email = 'dsf@dsf.com'
    user_password = '123'
    user_logged_in = False

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.wait_driver = WebDriverWait(cls.selenium, 10)

    def wait_element(self, by, req):
        return self.wait_driver.until(EC.presence_of_element_located((by, req)))

    @classmethod
    def create_user(cls):
        User.objects.create_user(cls.user_email, email=cls.user_email, password=cls.user_password)

    @classmethod
    def user_login(cls):
        if cls.user_logged_in:
            return

        print "user_login run..."
        cls.selenium.get('%s%s' % (os.getenv('DJANGO_LIVE_TEST_SERVER_ADDRESS'), '/'))
        username_input = cls.selenium.find_element_by_name("username")
        username_input.send_keys(cls.user_email)
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys(cls.user_password)
        cls.click = cls.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        cls.user_logged_in = True

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()
