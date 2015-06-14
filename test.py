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

class XmlTestCase(TestCase):
    def xml_compare(self, xml_true, xml_expected, excludes=[], parent='/'):
        if xml_true.tag != xml_expected.tag:
            xml_true.text
            raise AssertionError(
                'Tags do not match: <%s>%s != <%s>%s' % (parent, xml_true.tag, parent, xml_expected.tag))
        for name, value in xml_true.attrib.items():
            if not name in excludes:
                if xml_expected.attrib.get(name) != value:
                    raise AssertionError('Attributes do not match: <%s><%s %s=%r ..> != <%s><%s %s=%r ..>'
                                         % ( parent, xml_true.tag, name, value, parent,
                                             xml_expected.tag, name, xml_expected.attrib.get(name)))
        for name in xml_expected.attrib.keys():
            if not name in excludes:
                if name not in xml_true.attrib:
                    raise AssertionError('x2 has an attribute x1 is missing: %s' % name)
        if not self.text_compare(xml_true.text, xml_expected.text):
            raise AssertionError('text: %r != %r' % (xml_true.text, xml_expected.text))
        if not self.text_compare(xml_true.tail, xml_expected.tail):
            raise AssertionError('tail: %r != %r' % (xml_true.tail, xml_expected.tail))
        cl1 = xml_true.getchildren()
        cl2 = xml_expected.getchildren()

        i = 0
        for c1, c2 in zip(cl1, cl2):
            i += 1
            if not self.xml_compare(c1, c2, excludes, parent=xml_true.tag):
                raise AssertionError('children %i do not match: %s'
                                     % (i, c1.tag))
        return True

    def text_compare(self, t1, t2):
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()
