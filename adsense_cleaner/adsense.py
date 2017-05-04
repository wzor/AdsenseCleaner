# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#


"""Google AdSense selenium automation package.

This module making automation actions for Google AdSense web interface using 
selenium webdriver and web browser like Firefox or Chromium.
NOTICE: this package supports only English (EN) locale of AdSense 
interface at this time.

Google AdSense partners program Website: https://www.google.com/adsense
"""


from datetime import datetime
import os
import re
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from transliterate import translit 
except ImportError:
    message = ("Module 'adsense' has dependencies:\n"
               " - transliterate https://pypi.python.org/pypi/transliterate/"
               "Try this:\n"
               " $ pip install transliterate")
    raise SystemExit(message)


LOGIN_PAGE_URL = ('https://www.google.com/adsense/?hl=en&noaccount=false')
TMP_PATH = '{}/tmp/'.format(os.path.dirname(os.path.realpath(__file__)))


class AdSense(object):
    """Adsense interface automation methods."""
    
    def __init__(self, driver):
        self.wd = driver
        self.debug = True
        if not os.path.exists(TMP_PATH):
            os.makedirs(TMP_PATH)

    def msg(self, text=''):
        if self.debug:
            print text
    
    def error(self, text=''):
        self.wd.quit()
        raise SystemExit(text)
    
    def wait_for(self, locator, value, timeout=30):
        """Waiting for element to become visible."""
        try:
            WebDriverWait(self.wd, timeout).until(
                EC.visibility_of_element_located((locator, value))
                )
        except:
            msg_text = ("Error: timeout [{}] while waiting for element:\n"
                        "{} = {}"
                        ).format(timeout, locator, value)
            self.error(msg_text)
    
    def take_screenshot(self, name=''):
        """Create screenshot for entire browser window."""
        if not re.match('^[\-0-9a-z]+$', name, flags=re.IGNORECASE):
            name = name.replace('-', ' ')
            name = translit(name, reversed=True)
            name = name.replace("'", '')
        name = name.replace(' ', '-')
        t = datetime.now()
        self.wd.get_screenshot_as_file(
            '{}{}_{}_{}-{}_{}-{}.png'.format(
                TMP_PATH, t.day, t.month, t.year, t.hour, t.minute, name)
            )    
            
    def open_login_page(self):
        """Load Google AdSense login page."""
        self.wd.get(LOGIN_PAGE_URL)
        self.msg('[i] Login page loaded: {}'.format(LOGIN_PAGE_URL))

    def login(self, login='', password=''):
        """Login to AdSense interface."""
        self.wd.find_element(
                By.XPATH,
                ".//input[@aria-label='Email or phone']"
            ).send_keys(login + Keys.ENTER)
        sleep(1)
        passwd_xpath = ".//input[@aria-label='Enter your password']"
        self.wait_for(By.XPATH, passwd_xpath)
        self.wd.find_element(
                By.XPATH,
                passwd_xpath
            ).send_keys(password + Keys.ENTER)
        # Wait while interface will be loaded.
        self.wait_for(By.TAG_NAME, "as-app-header")
        self.msg(' +  Login OK, interface ready.')
        sleep(0.5)
    
    def open_main_menu(self):
        """Opening main menu in the sidebar."""
        if not self.wd.find_element(By.ID, 'sidebar-header-container').\
                is_displayed:
            self.wd.find_element(By.ID, 'as-menu-toggle').click()
            self.msg(' +  Sidebar menu opened.')
    
    def open_allow_and_block_ads_menu(self):
        """Open 'Allow & Block ADS' submenu."""
        self.wd.find_element(
                By.XPATH,
                (".//*[@id='allowblockads-section-header']"
                 "/div/div/div[@role='button']")
            ).click()
        self.wait_for(By.CLASS_NAME, "gbox-body")
        self.msg(' +  Allow & Block ADS menu opened.')
        sleep(0.5)
        
    def open_ads_review_center(self):
        """Open ADS review center tab."""
        # Clicking on tab 'Ad review center'.
        self.wd.find_element(By.PARTIAL_LINK_TEXT, 'Ad review center').click()
        # Wait while any ADS unit become visible (by default no filters active).
        self.wait_for(By.CLASS_NAME, "rhizo-model")
        self.msg(' +  ADS review center loaded.')
    
    def click_filter_button(self):
        """Clicking right side button 'Filters'."""
        self.wd.find_element(
                By.XPATH,
                ".//div[@class='arc-rhizo-main-panel']/div/div/div[1]/button[1]"
            ).click()
        
    def open_ads_review_filters(self):
        """Open filters settings in ads review centre.
        
        Will click filters button, then check if 'div' with text 'Ads matching' 
        is visible on the page. If not - make additional click on the button.
        """
        ads_matching_xpath = ".//div[text()='Ads matching']"
        self.click_filter_button()
        try:
            WebDriverWait(self.wd, 0.3).until(
                EC.visibility_of_element_located((By.XPATH, ads_matching_xpath))
                )
        except:
            self.click_filter_button()
        # Wait for 'Ads matching' text field to be visible.
        self.wait_for(By.XPATH, ads_matching_xpath)
       
    def block_all_visible_ads_units(self, block_adwords_accounts=False):
        """Blocking all ADS units on page in AdSense ads reiew centre."""
        # Check if ads units found.
        try:
            WebDriverWait(self.wd, 3).until(
                EC.visibility_of_element_located((
                    By.XPATH, ".//div[text()='No ads to display']"))
                )
            sleep(1)
            # No ads units found, exiting.
            return 0
        except:
            pass
        # Find all ADS containers.
        elements = self.wd.find_elements(By.CLASS_NAME, "rhizo-model")
        for element in elements:
            # Hover on ads unit (mouse over on 'star' img).
            star_img = element.find_element(
                By.XPATH, 
                ".//img[@title='Not starred']")
            ActionChains(self.wd).move_to_element(star_img).perform()
            sleep(0.1)
            # Check if ads unit already blocked.
            blocked_status = element.find_element(
                    By.XPATH,
                    ".//div[@class='arc-rhizo-action-bar-status']"
                ).text
            if not blocked_status == 'Blocked':
                # Block ADS unit by clicking on it's head container.
                element.find_element(
                        By.XPATH,
                        ".//div[@class='rhizo-stop-propagation']"
                    ).click()
                sleep(0.3)
            if block_adwords_accounts:
                # Check if [v] button available for ADS unit.
                # For tizers and other ads sources (not AdWords) [v] button
                # will not be available.
                try:
                    v_element = element.find_element(
                        By.XPATH, u".//div[text()='▾']/parent::button")
                except:
                    continue
                # Clicking on [v] button to open blocking options menu.
                v_element.click()
                # Waiting for link 'Block this AdWords account' and clicking it.
                anchor_xpath = ".//div/a[text()='Block this AdWords account']"
                WebDriverWait(self.wd, 0.3).until(
                    lambda e: element.find_element(By.XPATH, anchor_xpath
                        ).is_displayed(),
                    "Timeout while waiting: 'Block this AdWords account'."
                    )
                element.find_element(By.XPATH, anchor_xpath).click()
                sleep(0.2)
        return len(elements)
        
    def ads_review_block_units_by_keyword(
            self, keyword='', block_adwords_accounts=False, 
            max_pages=5, manual_mode=False):
        """Filtering ads units by keyword and blocking them."""
        if not keyword:
            return False
        self.open_ads_review_filters()
        # Entering filtering word in 'Ads matching' text field.
        filter_input = self.wd.find_element(
            By.XPATH,
            (".//div[text()='Ads matching']/"
             "following-sibling::input[@class='gwt-TextBox']")
            )
        self.msg(u' -> Filter = "{}"'.format(keyword))
        filter_input.clear()
        filter_input.send_keys(keyword + Keys.ENTER)
        if manual_mode:
            raw_input("Press ENTER when ready to review by the NEXT KEYWORD...")
            return True
        blocked_units_count = 0
        for page in range(max_pages):
            blocked_count = self.block_all_visible_ads_units(
                block_adwords_accounts)
            if blocked_count:
                self.msg(
                    u'[B] {} ads unit(s) blocked for keyword: "{}".'.\
                        format(blocked_count, keyword)
                    )
                # Take a time for browser to load ads units iframes content.
                if blocked_count <= 10:
                    sleep(3)
                # Make a screenshot for the page.
                self.take_screenshot(u'{}-{}'.format(keyword, page+1))
                blocked_units_count += blocked_count
            else:
                break
            # Check if next page available & go to it.
            next_button = self.wd.find_element(
                By.XPATH, ".//div/button[@title='Next ads']")
            if next_button.is_enabled():
                self.msg(' -> Loading next page: {}.'.format(page+2))
                next_button.click()
            else:
                break
        return blocked_units_count
  
    def logout(self):
        """AdSense Logout and closing the browser."""
        # Open user profile menu in the top right area.
        self.wd.find_element(
                By.XPATH,
                ".//header/span[3]/div/gaia-picker/div[@role='button']"
            ).click()
        sleep(1)
        # click 'Sign out'
        self.wd.find_element(
                By.XPATH,
                ".//gaia-picker-popup/div[2]/div/material-button[2]"
            ).click()
        sleep(3)
        self.wd.quit()

