import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import choice


def random_headers():
    '''
    Choose a random user_agent to use as an header for requests
    list of http header fields: https://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    '''
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36']

    # return {'User-Agent': choice(user_agents), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    return {'User-Agent': choice(user_agents), 'Accept': 'text/html'}


def make_dir(directory):
    '''
    Creates a directory if there is no directory
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("Directory already exist: {}. No action taken".format(directory))


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def requestForPage(url):
    '''
    Uses the requests libray and random_headers function
    to perform a GET request and return a page in text.
    The timeout per GET request is set to 5 secs
    '''
    # headers = {'User-Agent': ''}
    r = requests.get(url, headers=random_headers(), timeout=5)
    return r.text


def getBrowser():
    '''
    Uses Selenium and a pre-installed selenium chrome driver.
    Returns a haedless chrome browser  of window size 19200x1080 
    controlled by selenium
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver = os.path.join(
        os.getcwd(), 'seleniumdrivers', 'chromedriver')
    # print(chrome_driver)
    browser = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=chrome_driver)
    return browser


if __name__ == '__main__':
    pass
