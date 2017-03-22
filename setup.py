#!/usr/bin/env python
#
# Copyright (c) 2017-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

"""The setup package to install Adsense Cleaner with it's dependencies."""


from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name = 'AdsenseCleaner',
    version = '0.1',
    packages = find_packages(),
    
    description = "AdSense fraud ADS cleaner, Selenium based automation tool.",
    long_description = 
        "AdSense fraud ADS cleaner, Selenium based automation tool.",
        
    author = 'ph0x0en1x',
    author_email = 'ph0x0en1x@gmail.com',
    url = 'http://ph0en1x.net',
    
    license = "LICENSE.txt",
    keywords = "selenium automation ads adsense",
    
    platforms = ['linux'],
    install_requires = required,
)
