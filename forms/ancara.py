import time
from datetime import datetime

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from forms.base import BaseForm
from helpers import process_image

NAME = 'Елена'
FAMILY = 'Петрова'
FATHER_NAME = 'Владимировна'
PHONE = '+905001234567'
EMAIL = 'email@gmail.com'
DAY = '11'
MONTH = '11'
YEAR = '2000'
MR = 'MS'


class AncaraForm(BaseForm):
    url = 'https://ankara.kdmid.ru/queue/Visitor.aspx'

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

            self.driver.find_element(By.ID, 'ctl00_MainContent_txtFam').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtFam').send_keys(FAMILY)
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtIm').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtIm').send_keys(NAME)
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtOt').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtOt').send_keys(FATHER_NAME)
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtTel').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtTel').send_keys(PHONE)
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtEmail').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_txtEmail').send_keys(EMAIL)
            ##
            Select(self.driver.find_element(By.ID, 'ctl00_MainContent_DDL_Day')).select_by_value(DAY)
            Select(self.driver.find_element(By.ID, 'ctl00_MainContent_DDL_Month')).select_by_value(MONTH)
            self.driver.find_element(By.ID, 'ctl00_MainContent_TextBox_Year').clear()
            self.driver.find_element(By.ID, 'ctl00_MainContent_TextBox_Year').send_keys(YEAR)
            Select(self.driver.find_element(By.ID, 'ctl00_MainContent_DDL_Mr')).select_by_value(MR)
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
        self.driver.find_element(By.XPATH, '//a[@href="bpssp.aspx?nm=BIOPASSPORT"]').click()
        self.driver.find_element(By.ID, 'ctl00_MainContent_RList_0').click()
        self.driver.find_element(By.ID, 'ctl00_MainContent_ButtonA').click()
        self.driver.find_element(By.ID, 'ctl00_MainContent_CheckBoxList1_0').click()
        self.driver.find_element(By.ID, 'ctl00_MainContent_ButtonQueue').click()

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
