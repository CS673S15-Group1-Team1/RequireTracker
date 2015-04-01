# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestStory(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_story(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("___Test Project 2")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("___Test Project 2 Description")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_link_text("___Test Project 2").click()
        driver.find_element_by_link_text("Project Detail").click()
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("___Test Story 1")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("___Test Story 1")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("___Test Story 1 Description")
        driver.find_element_by_id("id_reason").clear()
        driver.find_element_by_id("id_reason").send_keys("___Reason")
        driver.find_element_by_id("id_test").clear()
        driver.find_element_by_id("id_test").send_keys("___Test")
        driver.find_element_by_id("id_hours").clear()
        driver.find_element_by_id("id_hours").send_keys("1")
        Select(driver.find_element_by_id("id_status")).select_by_visible_text("Started")
        Select(driver.find_element_by_id("id_points")).select_by_visible_text("3 Points")
        driver.find_element_by_id("id_pause").click()
        driver.find_element_by_id("id_pause").click()
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        self.assertRegexpMatches(driver.find_element_by_link_text("___Test Story 1").text, r"^___Test Story 1[\s\S]*$")
        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()
    
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