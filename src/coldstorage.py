import requests
import time
import os
import re
import glob

import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import random_headers, make_dir, log_error, getBrowser, requestForPage

from pymongo import MongoClient

BASE_URL = 'https://coldstorage.com.sg/'


def main():
    browser = getBrowser()
    pass


if __name__ == '__main__':
    main()
