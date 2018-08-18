# -*- coding: utf-8 -*-
import logging
import os
import glob
import json
import csv
from pathlib import Path

import click

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient


def getFiles(input_filepath):
    # get name of all the CSV files in /data/raw and store in result list
    os.chdir(input_filepath)
    results = [i for i in glob.glob('*.{}'.format('json'))]
    return results


def dataToDict(input_filepath):
    for file in getFiles(input_filepath):
        fullPath = os.getcwd() + "/" + file
        with open(fullPath, 'r') as fp:
            products = json.load(fp)
    return products


def dictToCSV(data):
    # By inspecting the img tag
    IMAGE_URL = 'https://s3-ap-southeast-1.amazonaws.com/media.redmart.com/newmedia/150x'
    productsList = []
    for _, pdtDetails in data.items():
        pdtID = pdtDetails['id']
        pdtSKU = pdtDetails['sku']
        pdtName = pdtDetails['title']
        pdtDesc = pdtDetails['desc']
        pdtImageURL = IMAGE_URL + str(pdtDetails['img']['name'])
        pdtPrice = pdtDetails['pricing']['price']
        pdtCountryOfOrigin = pdtDetails['details']['country_of_origin']
        try:
            pdtOrganic = pdtDetails['filters']['is_organic']
        except Exception as e:

            pdtOrganic = '0'
        pdtMfgName = pdtDetails['filters']['mfr_name']
        pdtBrandName = pdtDetails['filters']['brand_name']
        pdtStockStatus = pdtDetails['inventory']['stock_status']
        pdtURI = pdtDetails['details']['uri']
        pdtCategoryTags = pdtDetails['category_tags']
        productsList.append([pdtID, pdtName, pdtDesc, pdtImageURL, pdtPrice, pdtCountryOfOrigin,
                             pdtOrganic, pdtMfgName, pdtBrandName, pdtStockStatus, pdtURI, pdtCategoryTags])
        # print(pdtID, pdtName, pdtDesc,pdtImageURL, pdtPrice, pdtCountryOfOrigin, pdtOrganic, pdtMfgName, pdtBrandName, pdtStockStatus)
    return productsList


def toCSV(productsList, output_filepath):
    os.chdir(os.path.dirname(os.getcwd()) + '/processed')
    with open('data.csv', 'w+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for product in productsList:
            wr.writerow(product)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    productsDict = dataToDict(input_filepath)
    productsList = dictToCSV(productsDict)
    toCSV(productsList, output_filepath)

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
