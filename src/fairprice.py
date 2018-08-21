import requests
import time
import os
import re
import glob

import datetime
from bs4 import BeautifulSoup
from utils import random_headers, make_dir, log_error, getBrowser, requestForPage

from pymongo import MongoClient
filename = "data"
BASE_URL = 'https://www.fairprice.com.sg/'


def getProductLinks():
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
    print("Total number of root category links ", len(allCategoryRootLinks))
    #### End ####

    # Default File
    # soup = BeautifulSoup(open('home-care_liquid-detergents_delicate.html'), 'html.parser')

    #### Selenium start ####
    browser = getBrowser()

    #### Start - Getting all the products in the category ####
    allProductLinksinCategory = []
    for rootCategory in allCategoryRootLinks:
        browser.get(rootCategory)
        assert 'FairPrice' in browser.title
        print("====================")
        print(rootCategory)

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

        for link in soup.find_all('a'):
            try:
                if '/product/' in link.get('href') or 'FPProductDisplay?' in link.get('href'):
                    allProductLinksinCategory.append(link.get('href'))
            except:
                pass
    allProductLinksinCategory = set(allProductLinksinCategory)
    #### End - Getting all products in category ####
    print("total number of product links: ", len(allProductLinksinCategory))
    print("total time taken: ", time.time() - startTime)
    print("saving links")

    SAVEPATH = os.path.join(os.getcwd(), 'data', 'fairprice', 'raw')

    NOW = datetime.datetime.now()
    DATE = str(NOW.year).zfill(4) + \
        str(NOW.month).zfill(2) + str(NOW.day).zfill(2)

    # meta data for saving
    FILENAME = DATE + "_links"
    FMT = '.csv'
    SAVENAME = os.path.join(SAVEPATH, FILENAME+FMT)
    make_dir(SAVEPATH)
    with open(SAVENAME, 'w+') as fp:
        print("writing into csv: {}".format(os.path.abspath(SAVENAME)))
        for productLink in allProductLinksinCategory:
            fp.write(productLink + '\n')
    return allProductLinksinCategory, browser


def main():
    res = input(
        "Do you have a current .csv of product links you wish to load? (y/n): ")
    if res == 'y':
        browser = getBrowser()
        DATA_PATH = os.path.join(os.getcwd(), 'data', 'fairprice', 'raw')
        files = glob.glob(os.path.join(DATA_PATH, '*.csv'))
        for i, fp in enumerate(files):
            print("[{}]: {}".format(i, fp))
        chosen = int(
            input("Please choose a file: [0] - [{}]: ".format(len(files) - 1)))
        chosen_fp = files[chosen]
        print("Selected [{}]: {}".format(chosen, chosen_fp))

        with open(chosen_fp, 'r+') as fp:
            allProductLinksinCategory = []
            for link in fp.readlines():
                allProductLinksinCategory.append(link.strip())
    else:
        print("Generating a .csv of product links to scrape from.")
        print("This would rougly take around 35 mins depending on your")
        allProductLinksinCategory, browser = getProductLinks()

    # Start - Getting all attributes in product links
    client = MongoClient()
    db = client.Grocery
    fairprice = db.fairprice

    for productLink in allProductLinksinCategory:
        pdtDict = dict()
        print(productLink)
        browser.get(productLink)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        image_url = 'https://s3-ap-southeast-1.amazonaws.com/www8.fairprice.com.sg/fpol/media/images/product/XL/'
        pdtTitle = soup.find('h1').text
        pdtDict['Product_url'] = productLink
        pdtDict['Title'] = pdtTitle

        try:
            pdtWeightVol = soup.find('span',
                                     class_='pdt_weightMg').text.strip()
            pdtDict['Weight_Volume'] = pdtWeightVol
        except:
            pdtDict['Weight_Volume'] = "NA"

        pdtDict['Selling_Price'] = soup.find(
            'span', class_='pdt_C_price').text.strip()
        try:
            pdtDict['Original_Price'] = soup.find(
                'span', class_='pdt_O_price').text.strip()
        except:
            pdtDict['Original_Price'] = soup.find(
                'span', class_='pdt_C_price').text.strip()
        try:
            text = soup.find(
                'div', class_='pdt_desc_d_row pdpDesc clearfix').p.text.strip()
            if '•' in text:
                pdtDict['Key Info'] = text.split('•')[1:]
            else:
                pdtDict['Key Info'] = text
        except:
            pdtDict['Key Info'] = '0'

        for i in soup.find_all('div', class_='pdt_desc_d_row clearfix'):
            try:
                header = i.find('div', class_='pdr_name').text.strip()
            except:
                header = 'DISCLAIMER'
            try:
                content = i.find('div', class_='pdr_p_desc').text.strip()
            except:
                content = 'This site and all information contained herein is provided on a "as is" without any implied or express warranty including of any implied warranty as to title, quality, merchantability, fitness for purpose, or non-infringement. Before acting on the information found on FairPrice On website, you may wish to confirm the facts that are important to your decision making. Product information on our website may be different from information on the products for a variety of reasons including such things as manufacturers'
            if len(header) == 0:
                content = i.find('div', class_='pdr_p_desc').text
                cleaned_text = []
                for char in re.sub('\s+', ' ', content).split(' '):
                    if len(char) > 1:
                        cleaned_text.append(char)
                pdtDict[cleaned_text[0]] = cleaned_text[1:]
            else:
                pdtDict[header] = content
        print("Pdt Dict")
        print(pdtDict)
        fairprice.insert(pdtDict)

    browser.quit()
    #### Selenium end ####

    print("Time taken to run:", str(time.time() - startTime))


if __name__ == '__main__':
    main()
