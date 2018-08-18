import os
import glob
import time
import json

from pymongo import MongoClient

if __name__ == '__main__':
    data_path = os.path.join(os.getcwd(), 'data', 'raw')
    raw_jsons = glob.glob(os.path.join(data_path, '*.json'))

    print("Please select a raw data.json to put into mongodb")
    for i, file in enumerate(raw_jsons):
        print('[{}]: {}'.format(i, file))
    selected = int(
        input("Input number from 0 - {}: ".format(len(raw_jsons) - 1)))
    print("selected [{}]: {}".format(selected, raw_jsons[selected]))
    # time.sleep(5)
    with open(raw_jsons[selected]) as fp:
        selected_json = json.load(fp)

    client = MongoClient()
    db = client.Grocery
    redmart = db.redmart
    for pdtDetails in selected_json.values():
        IMAGE_URL = 'https://s3-ap-southeast-1.amazonaws.com/media.redmart.com/newmedia/150x'
        try:
            pdtOrganic = pdtDetails['filters']['is_organic']
        except Exception as e:
            pdtOrganic = '0'
        row = {
            'pdtID': pdtDetails['id'],
            'pdtSKU': pdtDetails['sku'],
            'pdtName': pdtDetails['title'],
            'pdtDesc': pdtDetails['desc'],
            'pdtImageURL': IMAGE_URL + str(pdtDetails['img']['name']),
            'pdtPrice': pdtDetails['pricing']['price'],
            'pdtCountryOfOrigin': pdtDetails['details']['country_of_origin'],
            'pdtOrganic': pdtOrganic,
            'pdtMfgName': pdtDetails['filters']['mfr_name'],
            'pdtBrandName': pdtDetails['filters']['brand_name'],
            'pdtStockStatus': pdtDetails['inventory']['stock_status'],
            'pdtURI': pdtDetails['details']['uri'],
            'pdtCategoryTags': pdtDetails['category_tags']
        }
        redmart.insert(row)
