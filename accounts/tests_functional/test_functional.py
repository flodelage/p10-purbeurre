
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui


class ResetPasswordTest(LiveServerTestCase):

    def test_reset_password(self):
        driver = webdriver.Chrome('/Users/floriandelage/Downloads/chromedriver')
        action = ActionChains(driver)

        driver.get('http://127.0.0.1:8000/')

        login_a = driver.find_element_by_id('login_link')
        action.click(login_a).perform()
        assert '/accounts/login' in driver.current_url

        reset_a = driver.find_element_by_id('reset_link')
        action.click(reset_a).perform()
        assert '/accounts/password_reset' in driver.current_url

        email_input = driver.find_element_by_id('id_email')
        email_input.send_keys('test@django.com')
        email_input.send_keys(Keys.RETURN)
        assert '/password_reset/done' in driver.current_url
