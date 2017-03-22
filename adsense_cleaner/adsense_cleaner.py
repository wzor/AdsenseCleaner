#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For installation and usage instructions see the README file.


"""Google AdSense Fraud ADS Cleaner automation program for web interface.

This programm not modifying any of scripts or elements in AdSense's web 
interface, it just emulating user actions for filtering and blocking ADS units.
"""


from datetime import datetime
import getpass
import operator

from adsense import AdSense
from config import config

try:
    from selenium import webdriver
except ImportError:
    message = ("Module webdriver_firefox has dependencies:\n"
               " - selenium https://pypi.python.org/pypi/selenium\n"
               "Try this:\n"
               " $ pip install selenium==2.53.0")
    raise SystemExit(message)
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class AdsenseCleaner(object):
    """Adsense Cleaner class."""
    
    def __init__(self):
        self.wd = None
        self.adsense = None
        self.maximize_window = True
        self.implicitly_wait_sec = 10
        t = datetime.now()
        message = ("Start time is:\n {}-{}-{} {}:{}\n\n"
                   "The work plane for now:\n"
                   " {} words for blocking ADS units + AdWords Accounts,\n"
                   " {} words for blocking only ADS units,\n"
                   " {} words for reviewing ADS by hands.\n\n"
                   "So, let's do it...\n"
                   )
        print message.format(
            t.day, t.month, t.year, t.hour, t.minute,
            len(config['words_block_units_and_accounts']),
            len(config['words_block_units']),
            len(config['words_block_manual_mode'])
            )

    def prepare_driver(self):
        """Prepare WebDriver and init the AdSense object."""
        if config['webdriver'] == 'firefox':
            profile = webdriver.FirefoxProfile()
            profile.native_events_enabled = False
            if config['firefox_binary_path']:
                binary = FirefoxBinary(config['firefox_binary_path'])
                self.wd = webdriver.Firefox(profile, firefox_binary=binary)
            else:
                self.wd = webdriver.Firefox(profile)
            if self.maximize_window:
                self.wd.maximize_window()
        elif config['webdriver'] == 'chromium':
            self.wd = webdriver.Chrome()
        else:
            raise SystemExit("Error: invalid webdriver specified in config.")
        self.adsense = AdSense(self.wd)
        self.wd.implicitly_wait(self.implicitly_wait_sec)

    def run(self):
        """Running AdSense automation operations."""
        stats = {
            'bad_words': {},
            'adwords_accounts': 0,
            }
        if not config['adsense_login']:
            config['adsense_login'] = raw_input("Enter your AdSense LOGIN: ")
        if not config['adsense_password']:
            config['adsense_password'] = getpass.getpass(
                "Enter you AdSense PASSWORD: ")
        if not config['adsense_login'] or not config['adsense_password']:
            raise SystemExit(
                "Error: invalid (empty) login or password. Please, try again.")
        self.prepare_driver()
        self.adsense.open_login_page()
        self.adsense.login(config['adsense_login'], config['adsense_password'])
        self.adsense.open_main_menu()
        self.adsense.open_allow_and_block_ads_menu()
        self.adsense.open_ads_review_center()
        
        # Block units & adwords accounts (auto).
        for bad_word in config['words_block_units_and_accounts']:
            blocked_count = self.adsense.ads_review_block_units_by_keyword(
                bad_word,
                block_adwords_accounts=True,
                max_pages=5
                )
            stats['adwords_accounts'] += blocked_count
            stats['bad_words'][bad_word] = blocked_count
            
        # Block only units (auto).
        for bad_word in config['words_block_units']:
            blocked_count = self.adsense.ads_review_block_units_by_keyword(
                bad_word,
                block_adwords_accounts=False,
                max_pages=5
            )
            stats['bad_words'][bad_word] = blocked_count
                
        # Review and block units (by hands with some automation).
        for bad_word in config['words_block_manual_mode']:
            self.adsense.ads_review_block_units_by_keyword(
                bad_word,
                manual_mode=True
            )
            
        print ("\n\nBad words stats:\n"
               "[word - blocked units count]")
        total = 0
        # Sort dict elements by values + store in a list with (k,v) pairs.
        sorted_words = sorted(stats['bad_words'].items(), 
            key=operator.itemgetter(1))
        sorted_words.reverse()
        for word_data in sorted_words:
            key = word_data[0]
            count = word_data[1]
            print u" {} - {}".format(key, count)
            total += count
        print "\nADS units blocked: {}".format(total)
        print "AdWords accounts blocked: {}\n".format(stats['adwords_accounts'])
        raw_input("Done. \nPress ENTER to EXIT...")
        self.adsense.logout()


def main():
    app = AdsenseCleaner()
    app.run()


if __name__ == '__main__':
    main()
