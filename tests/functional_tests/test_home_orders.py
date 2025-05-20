from django.test import LiveServerTestCase
from utils.browser import make_firefox_driver
import time
from selenium.webdriver.common.by import By


class OrdersBaseTest(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.driver = make_firefox_driver()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()


class OrderPageFunctionalTest(OrdersBaseTest):
    def test_home_page(self):
        self.driver.get(self.live_server_url)
        time.sleep(2)  # Wait for the page to load

        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIn("Clique para acessar o sistema", body.text)
