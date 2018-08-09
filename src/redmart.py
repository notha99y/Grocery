'''
Script that scrap redmart

Business question:
https://blog.moneysmart.sg/shopping/online-grocery-shopping-in-singapore/
'''

import requests
import json
import time
import math
import os
import datetime

now = datetime.datetime.now()
date = str(now.year).zfill(4) + str(now.month).zfill(2) + str(now.day).zfill(2)


# FILENAME = str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime()))
FILENAME = date + "_data"
FMT = '.json'
SAVEPATH = os.path.join(os.getcwd(), 'data', 'raw', FILENAME+FMT)

VERSION = 'v1.6.0'
PAGESIZE = 100


def requestForProducts(val, page):
    r = requests.get(
        'https://api.redmart.com/{}/catalog/search?category={}&pageSize={}&page={}'.format(
            VERSION, val, PAGESIZE, page))
    data = json.loads(r.text)
    return data


def main(output_filepath):
    startTime = time.time()

    r = requests.get(
        'https://api.redmart.com/{}/catalog/search?extent=0&depth=1'.format(VERSION))  # gives the category
    data = json.loads(r.text)  # similarily can use data = r.json()

    # uri = [x['uri'] for x in data['categories']]
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
            data = requestForProducts(val, 0)
            sleep_time = 5  # in units of seconds
            print("Sleep for {} secs".format(sleep_time))
            time.sleep(sleep_time)
            print('[Category]', str(val), '[Total items]', data['total'])
            # try:
            #     # print('[Category]', str(val), 'Total', data['total'], 'Page', data['page'], 'Page Size', data['page_size'])
            #     print('[Category]', str(val), '[Total items]', data['total'])
            # except KeyError:
            #     continue
            # else:
            #     pass

            if data['total'] <= 100:
                # print(data['products'][0]['title'])
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
                    except KeyError:
                        pass
        print(len(productsDict))
        # print("./data/raw/{}.txt".format(FILENAME))
        with open(SAVEPATH, 'w+') as fp:
            print("writing into json: {}".format(os.path.abspath(SAVEPATH)))
            try:
                existingProductsDict = json.load(fp)
                existingProductsDict.update(productsDict)
                json.dump(productsDict, fp)
            except BaseException:
                json.dump(productsDict, fp)

    print("Time taken to run:", str(time.time() - startTime))


if __name__ == '__main__':
    main('.')
