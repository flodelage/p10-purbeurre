
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui


class HomeSearchTest(LiveServerTestCase):

    def test_home_autocomplete(self):
        driver = webdriver.Chrome('/Users/floriandelage/Downloads/chromedriver')
        action = ActionChains(driver)

        driver.get('http://127.0.0.1:8000/')

        #populate the input with data
        autocomplete_input = driver.find_element_by_class_name('autocomplete-input')
        autocomplete_input.send_keys('Nutella')
        action.pause(3)
        #click on the ul
        ul = driver.find_element_by_id('autocomplete-result-list-1')
        action.click(ul).perform()

        assert 'Nutella' in driver.page_source or 'nutella' in driver.page_source or 'NUTELLA' in driver.page_source


class AllProductsListTest(LiveServerTestCase):

    def test_all_products_list_pagination(self):
        driver = webdriver.Chrome('/Users/floriandelage/Downloads/chromedriver')
        action = ActionChains(driver)

        driver.get('http://127.0.0.1:8000/catalog/all_products/')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_two = driver.find_element_by_id('page_2')
        action.pause(3)
        action.move_to_element(page_two).click().perform()

        assert '/catalog/all_products/?page=2' in driver.current_url
