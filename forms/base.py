import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)


class BaseForm:
    url = ''

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def ddos_title_exists(self) -> bool:
        elements = self.driver.find_elements(By.TAG_NAME, 'title')
        for elem in elements:
            if elem.text == 'DDOS-GUARD':
                return True
        return False

    def save_info(self, folder):
        ts = int(datetime.now().timestamp())
        self.driver.save_screenshot(f'{folder}/{ts}.png')
        with open(f'{folder}/{ts}.html', 'w') as html:
            html.write(self.driver.page_source)

    def process(self):
        raise NotImplementedError()
