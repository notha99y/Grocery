'''
Script that scrap redmart

Business question:
https://blog.moneysmart.sg/shopping/online-grocery-shopping-in-singapore/

Other business questions:
-
-
'''

import requests
import json
import time
import math
import os
import datetime
import random
from utils import make_dir, log_error

# getting the date in YYYYMMDD format
NOW = datetime.datetime.now()
DATE = str(NOW.year).zfill(4) + str(NOW.month).zfill(2) + str(NOW.day).zfill(2)

# meta data for saving
FILENAME = DATE + "_data"
FMT = '.json'
SAVEPATH = os.path.join(os.getcwd(), 'data', 'redmart', 'raw')
SAVENAME = os.path.join(SAVEPATH, FILENAME+FMT)

# meta data for requests
VERSION = 'v1.6.0'
PAGESIZE = 100


def requestForProducts(val, page):
    num_of_retries = 3
    sleep_time = 3  # in units of seconds
    while num_of_retries > 0:
        try:
            r = requests.get(
                'https://api.redmart.com/{}/catalog/search?category={}&pageSize={}&page={}'.format(
                    VERSION, val, PAGESIZE, page), timeout=5)
            data = json.loads(r.text)
            return data
        except Exception as e:
            log_error("Get Request Error: {}".format(e))
            time.sleep(sleep_time)
            print("Num of retries left: {}, sleep for {} secs".format(
                num_of_retries, sleep_time))
            num_of_retries -= 1
            sleep_time *= 3
    return None


def main(output_filepath):
    startTime = time.time()

    r = requests.get(
        'https://api.redmart.com/{}/catalog/search?extent=0&depth=1'.format(VERSION), timeout=5)  # gives the category
    data = json.loads(r.text)  # similarily can use data = r.json()

    uriDict = {}  # Uniform Resource Identifier
    for x in data['categories']:
        for y in x['children']:
            try:
                uriDict[x['uri']].append(y['uri'])
            except KeyError:
                uriDict[x['uri']] = [y['uri']]
    productsDict = {}
    for key in uriDict:
        for val in uriDict[key]:
            # sleep_time = random.uniform(0.5, 5)  # in units of seconds
            # time.sleep(sleep_time)
            # print("Sleep for {} secs".format(sleep_time))

            data = requestForProducts(val, 0)
            if type(data) == None:
                log_error("Get Request Failed")
                continue

            print('[Category]', str(val), '[Total items]', data['total'])

            if data['total'] <= 100:
                for product in data['products']:
                    productsDict[product['title']] = product
            else:  # crawl to next page
                pages = math.ceil(data['total'] / PAGESIZE)
                for page in range(pages):
                    try:
                        data = requestForProducts(val, page)
                        # print(data['products'][0]['title'])
                        for product in data['products']:
                            productsDict[product['title']] = product

                    except KeyError as e:
                        print("Page {} loaded without products".format(page))
                        log_error(str(e))
                        continue
        print(len(productsDict))

        make_dir(SAVEPATH)
        with open(SAVENAME, 'w+') as fp:
            print("writing into json: {}".format(os.path.abspath(SAVENAME)))
            try:
                existingProductsDict = json.load(fp)
                existingProductsDict.update(productsDict)
                json.dump(productsDict, fp)
            except BaseException:
                json.dump(productsDict, fp)

    print("Time taken to run:", str(time.time() - startTime))


if __name__ == '__main__':
    main('.')
