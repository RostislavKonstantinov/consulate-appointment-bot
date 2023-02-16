import time
from datetime import datetime

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from forms.base import BaseForm
from helpers import process_image


class AncaraQueueForm(BaseForm):
    url = 'https://ankara.kdmid.ru/queue/orderinfo.aspx?id=123456&cd=046dd51b&ems=1E024FCC'

    def main_form(self):
        self.logger.info(f'{datetime.now()} Start main_form')
        finish = False
        while not finish:
            time.sleep(2)
            try:
                capcha = self.driver.find_element(By.ID, 'ctl00_MainContent_imgSecNum')
            except NoSuchElementException:
                self.driver.refresh()
                continue

            capche_binary = capcha.screenshot_as_png
            capcha_value = process_image(capche_binary)
            self.logger.info(f'Capcha: {capcha_value}')
            if len(capcha_value) != 6:
                self.driver.refresh()
                continue

            self.driver.find_element(By.ID, 'ctl00_MainContent_txtCode').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtCode').send_keys(capcha_value)

            self.driver.find_element(By.ID, 'ctl00_MainContent_ButtonA').click()

            try:
                if self.driver.find_element(By.ID, 'ctl00_MainContent_lblCodeErr'):
                    self.logger.info(f'{datetime.now()} Capcha was wrong')
                    with open(f'wrong/{capcha_value}.png', 'wb') as f:
                        f.write(capche_binary)
                    self.driver.save_screenshot(f'wrong/window-{capcha_value}.png')
                    self.driver.refresh()
                    continue
            except NoSuchElementException:
                pass

            finish = True

    def choose_reason(self):
        self.logger.info(f'{datetime.now()} Start choose_reason')
        self.driver.find_element(By.ID, 'ctl00_MainContent_ButtonB').click()

    def process_result(self):
        self.logger.info(f'{datetime.now()} Start process_result')
        panel = self.driver.find_element(By.ID, 'center-panel')
        panel.find_elements(By.TAG_NAME, 'p')
        for p in panel.find_elements(By.TAG_NAME, 'p'):
            if p.text.startswith('К сожалению, в настоящий момент на интересующее Вас консульское действие нет свободных мест'):
                self.logger.info(f'No places .( {datetime.now()}')
                self.save_info('places')
                return
            else:
                raise ValueError('Slot found!!!')

    def process(self):
        self.driver.get(self.url)
        self.main_form()
        self.choose_reason()
        self.process_result()
