import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    # instalar el webdriver de chrome
    _driver = webdriver.Chrome(ChromeDriverManager().install())

    # navegar a amazon.com
    _driver.get("https://www.amazon.com.mx")

    # tiempo de espera para el cargado del DOM en la primera pagina
    _driver.implicitly_wait(10)

    yield _driver

    _driver.quit()


def test_search_box(driver):

    search_word = "Videojuegos"

    # obtiene el searchbox del DOM
    search_box = driver.find_element_by_id("twotabsearchtextbox")

    # escribe en el searchbox
    search_box.send_keys(search_word)

    # obtiene el button del DOM
    submit_button = driver.find_element_by_xpath("//input[@type='submit' and @class='nav-input']")

    # da click en el button
    submit_button.click()

    # tiempo de espera para el cargado del DOM despues de una redireccion
    span_message = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//span[@class='a-color-state a-text-bold']"))
    )

    # validamos que la palabra buscada sea igual al texto del span
    search_word == span_message.text.replace("\"", "")

    # validamos que la palabra buscada este en el titulo
    assert search_word in driver.title

    # validamos que la palabra buscada este en la url actual
    assert search_word in driver.current_url


def test_search_bestsellers(driver):

    search_word = "Los más vendidos"

    # obtiene el button del DOM
    best_sellers_button = driver.find_element_by_xpath("//a[@href='/gp/bestsellers/?ref_=nav_cs_bestsellers']")

    # da click en el button
    best_sellers_button.click()

    # tiempo de espera para el cargado del DOM despues de una redireccion
    best_sellers_link = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//div/a[@href='https://www.amazon.com.mx/gp/bestsellers/ref=zg_bs_tab']")
        )
    )

    assert search_word in driver.title
    assert search_word == best_sellers_link.text
