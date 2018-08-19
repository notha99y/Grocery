import requests
import json
import time
import math
import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import random_headers, make_dir, log_error

filename = "data"
BASE_URL = 'https://www.fairprice.com.sg/'


def requestForPage(url):
    # headers = {'User-Agent': ''}
    r = requests.get(url, headers=random_headers(), timeout=5)
    return r.text


def main():
    startTime = time.time()

    # Default File
    # soup = BeautifulSoup(open('fairprice.html'), 'html.parser')

    # Live Server
    soup = BeautifulSoup(requestForPage(BASE_URL), 'lxml')

    topLevelLinks = set([link.get('href')
                         for link in soup.find_all('a', {'class': 'selSecondNav'})])

    allLinks = set([link.get('href') for link in soup.find_all('a')])

    allCategoryLinks = sorted(set(
        [link for topLevelLink in topLevelLinks for link in allLinks if topLevelLink is not None and link is not None and topLevelLink in link]))

    #### Start - To get all the root links + remove top and second layer links ####
    allCategoryRootLinks = []
    for x in allCategoryLinks:
        tempList1 = []
        for y in allCategoryLinks:
            if y in x and len(y) < len(x):
                tempList1.append(x)
        if len(tempList1) > 1:
            allCategoryRootLinks.append(tempList1[-1])

    allCategoryRootLinks = sorted(set(allCategoryRootLinks))
    #### End ####

    # Default File
    # soup = BeautifulSoup(open('home-care_liquid-detergents_delicate.html'), 'html.parser')

    #### Selenium start ####
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver = os.path.join(
        os.getcwd(), '..', 'WebScraping', 'seleniumdrivers', 'chromedriver')
    # print(chrome_driver)
    browser = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=chrome_driver)

    for rootCategory in allCategoryRootLinks:
        browser.get(rootCategory)
        assert 'FairPrice' in browser.title
        print("====================")
        print(rootCategory)
        pageSize = 0
        soup = BeautifulSoup(browser.page_source, 'lxml')
        while True:
            if 'prodLoadMoreBck hide_element'in browser.page_source:
                print("Hide Element")

                break
            elif 'prodLoadMoreBck' in browser.page_source and soup.find('div', id='noFilterMsg')['class'][0] == 'hidden':
                print("need to click")
                try:
                    browser.find_element_by_link_text('LOAD MORE').click()
                except:
                    print("didnt manage to click")
                    pass
            else:
                break

        #### Start - Getting all the products in the category ####
        allProductLinksinCategory = []
        for link in soup.find_all('a'):
            try:
                if '/product/' in link.get('href') or 'FPProductDisplay?' in link.get('href'):
                    allProductLinksinCategory.append(link.get('href'))
            except:
                pass
        allProductLinksinCategory = set(allProductLinksinCategory)
        for count, x in enumerate(allProductLinksinCategory):
            print(count, x)
        #### End - Getting all products in category ####

    browser.quit()
    #### Selenium end ####

    print("Time taken to run:", str(time.time() - startTime))


if __name__ == '__main__':
    main()
