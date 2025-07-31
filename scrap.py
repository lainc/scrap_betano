# from time import sleep
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# from pathlib import Path


html_header = "<html>\n<head>\n\t<title>missing images</title>\n<head>\n<body>\n"
html_ender  = "</body>\n</html>\n"
# url = r'https://www.betano.bet.br'
url = r'https://www.betano.bet.br/sport/futebol/ligas/'

estimated_fetch_time = 7
def get_driver():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = Firefox(options=options)
    driver.implicitly_wait(estimated_fetch_time)
    return driver


def printa(msg, out):
    out.write(msg + "\n")

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
    x_btn.click()

def get_leagues(driver):
    out = open("out.txt", "w")
    printa('init', out)
    league_containers = driver.find_element(By.CSS_SELECTOR, '.sport-block')
    leagues = leagues_containers.find_elements(By.XPATH, "./div")[1:-1] # filhos de .sport-block
    league_css = 'div:nth-child(1) > div:nth-child(2)'
    leagues = [ l.find_element(By.CSS_SELECTOR, league_css) for l in leagues ] # pai de Brasil na lista
    i = j = 0
    for league in leagues:
        comps = league.find_elements(By.XPATH, "./div")
        for comp in comps:
            # a = comp.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(1) > a:nth-child(2)')
            a = comp.find_element(By.XPATH, "./div[1]/div[1]/a")
            print(a.text)
            printa(f'{"-"*20}\n{a.text}', out)
            printa(f'{a.get_attribute("innerHTML")}\n{"-"*20}\n', out)
            i += 1
            if i == 2:
                break
        j += 1
        if j == 2:
            break
            # link = comp.find_element(By.TAG_NAME, 'a')
            # print(link.get_attribute("href"))
    out.close()


def main():
    driver = get_driver()
    driver.get(url)

    close_popups(driver)
    get_leagues(driver)


if __name__ == '__main__':
    print('init')
    main()
