# import requests
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Accept-Language':	'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Host': 'ankara.kdmid.ru',
#     'Cookie': '__ddg1_=2uYAVMXi0QoMCgh6EMog; ASP.NET_SessionId=bljb1j55tscpgyn4iwwyux45',
# }
# resp = requests.get('https://ankara.kdmid.ru/queue/CodeImage.aspx', headers=headers, allow_redirects=True)
# print(resp.content)
from selenium import webdriver
import time
import numpy as np
import cv2

# Main Function
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import helpers

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1420,1080')
    options.add_argument("--incognito")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="chromedriver",
                              options=options)
    total = 0
    for i in range(5):
    # i = 1
    # Send a get request to the url
        driver.get('https://ankara.kdmid.ru/queue/CodeImage.aspx')
        print(driver.page_source)
        time.sleep(2)
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        # image = driver.find_element(By.TAG_NAME, 'img').screenshot_as_png
        image = myElem.screenshot_as_png
        nparr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        img = helpers.remove_noise(img)
        img = helpers.thresholding(img)
        cv2.imwrite(f'images/{i}.png', img)
        result = helpers.to_str(img).strip()
        total += bool(len(result) == 6)
        print(i, '>>>>', result, len(result) == 6)
    driver.quit()
    print("Done", total, total/199)
