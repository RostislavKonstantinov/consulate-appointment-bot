import time

from selenium import webdriver
from selenium.common import NoSuchElementException

from forms import AncaraForm, AncaraQueueForm

def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--window-size=1420,1080')
    options.add_argument("--incognito")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="chromedriver",
                              options=options)
    return driver


# Main Function
if __name__ == '__main__':
    driver = get_driver()
    # forms = [AncaraForm(driver)]
    forms = [AncaraQueueForm(driver)]
    try:
        while True:
            for form in forms:
                try:
                    form.process()
                except NoSuchElementException as ex:
                    form.logger.exception('Element not found.')
                    form.save_info('errors')
            # time.sleep(30)
    except Exception:
        ts = int(time.time())
        driver.save_screenshot(f'results/{ts}.png')
        with open(f'results/{ts}.html', 'w') as html:
            html.write(driver.page_source)
        raise
    finally:
        driver.quit()
