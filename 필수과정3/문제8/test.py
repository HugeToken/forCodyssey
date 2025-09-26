from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
import time

browser = webdriver.Chrome()

URL = 'https://nid.naver.com/nidlogin.login'
browser.get(URL)

id_value = os.environ.get('NAVER_ID')
password_value = os.environ.get('NAVER_PW')

try:
    wait = WebDriverWait(browser, 10)

    browser.execute_script("document.getElementsByName('id')[0].value = arguments[0];", id_value)
    browser.execute_script("document.getElementsByName('pw')[0].value = arguments[0];", password_value)

    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'log.login')))
    login_btn.click()

    time.sleep(3)

    mail_url = 'https://mail.naver.com/v2/folders/0/all'
    browser.get(mail_url)

    selector = 'div.mail_title a.mail_title_link span.text'
    elems = []
    try:
        elems = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    except TimeoutException:
        pass

    if not elems:
        print('요청한 시간 내에 메일 제목 요소를 찾지 못했습니다.')
    else:
        for i, el in enumerate(elems, start=1):
            title = el.text.strip()
            if title:
                print(f'{i}. {title}')

except Exception as e:
    print(f'에러가 발생했습니다: {e}')
finally:
    browser.quit()