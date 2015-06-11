# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

POSTCODES = {   "mk429gn" = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72],
                "mk429gl" = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63],

            }
class AddressChecker(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.dslchecker.bt.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_address_checker(self):
        for postcode in POSTCODES:
            for x in range(1,3):
                print "Checking address {0} {1}".format(str(x), postcode)
                driver = self.driver
                driver.get(self.base_url)
                driver.find_element_by_link_text("Address Checker").click()
                driver.find_element_by_css_selector("input.form_button").click()
                driver.find_element_by_name("PostCode").clear()
                driver.find_element_by_name("PostCode").send_keys(postcode)
                driver.find_element_by_name("buildingnumber").clear()
                driver.find_element_by_name("buildingnumber").send_keys(str(x))
                driver.find_element_by_css_selector("input.form_button").click()
                self.driver.implicitly_wait(10)
                self.assertEqual("WBC FTTP", driver.find_element_by_xpath("//tr[2]/td/span").text,"{0} {1} is not FTTP enabled".format(str(x), postcode))
                time.sleep(5)

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
