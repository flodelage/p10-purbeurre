
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui


class HomeTest(LiveServerTestCase):

  def home_autocomplete_test(self):
    driver = webdriver.Chrome('/Users/floriandelage/Downloads/chromedriver')
    action = ActionChains(driver)
    wait = ui.WebDriverWait(driver, 1000)
    # wait.until(lambda driver: driver.find_element_by_tag_name("iframe").is_displayed())

    driver.get('http://127.0.0.1:8000/')

    #populate the input with data
    autocomplete_input = driver.find_element_by_class_name('autocomplete-input')
    autocomplete_input.send_keys('Nutella')

    #click on the ul
    ul = driver.find_element_by_id('autocomplete-result-list-1')
    action.click(ul).perform()

    assert 'Nutella' in driver.page_source
