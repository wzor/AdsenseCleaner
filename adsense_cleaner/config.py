# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# For installation and usage instructions see the README file.


config = {
    # Your AdSense authentication data.
    'adsense_login': '',
    'adsense_password': '',
    
    # Webdriver to use: firefox|chrome
    'webdriver': 'firefox',
    # Firefox binary path if you want to use other than installed version.
    'firefox_binary_path': '/home/user/tmp/firefox_45/firefox',
    
    # Bad words list to block all matched ads and it's AdWords accounts.
    'words_block_units_and_accounts': [
        u'плохое слово',
        u'мат перемат',
        u'железобетонный ст0як',
        u'папПил0мы',
        ],
    
    # Bad words list to block all matched ads only.
    'words_block_units': [
        u'проблемы исчезнут',
        ],
    
    # Bad words list to review them by hands with iterations automation.
    'words_block_manual_mode': [
        u'бесплатно',
        u'скачать',
        ],
    }
