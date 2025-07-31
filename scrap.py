from time import sleep
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# from pathlib import Path


html_header = "<html>\n<head>\n\t<title>missing images</title>\n<head>\n<body>\n"
html_ender  = "</body>\n</html>\n"
url = r'https://www.betano.bet.br'

estimated_fetch_time = 7
def get_driver():
    options = FirefoxOptions()
    # options.add_argument("--headless=new")
    driver = Firefox(options=options)
    driver.implicitly_wait(estimated_fetch_time)
    return driver

# <button id="onetrust-accept-btn-handler">SIM, EU ACEITO</button>
# <button class="button-class tw-border-n tw-border-solid tw-bg-n-22-licorice tw-border-n-28-cloud-burst tw-text-white-snow tw-uppercase tw-font-bold tw-p-nm tw-rounded-s tw-w-full" data-qa="age-verification-modal-ok-button"><span>Sim</span></button>
def close_popups(driver):
    errors = [NoSuchElementException]
    wait = WebDriverWait(driver, timeout=6, poll_frequency=.2, ignored_exceptions=errors)

    # sim no aceitar cookies
    ok_btn_id = "onetrust-accept-btn-handler"
    acc_cookies = driver.find_element(By.ID, ok_btn_id)
    acc_cookies.click()

    # sim no "acima de 18"
    age_check_pane = driver.find_element(By.ID, "age-verification-modal")
    wait.until(lambda _ : age_check_pane.is_displayed())
    age_check_btns = age_check_pane.find_elements(By.TAG_NAME, "button")
    yes_btn = age_check_btns[1]
    yes_btn.click()

    # fechar painel de registramento
    x_btn_css = '.button-close'
    x_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, x_btn_css)))
    print(x_btn.text)
    x_btn.click()


def main():
    driver = get_driver()
    driver.get(url)

    close_popups(driver)


if __name__ == '__main__':
    main()
