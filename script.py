from bs4 import BeautifulSoup
from selenium import webdriver

async def launch_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get('https://web.whatsapp.com')

async def start_scrape():
    """ This is a test function which will contain the possible scraping ways"""
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    a = soup.findAll("div", {"id": "pane-side"})[0] #This will fecth all the life side panel's code
    soup = BeautifulSoup(a, 'lxml')
    _list = soup.findAll('div', {'tabindex' : '-1'})[1:] #This _list will contain all the chats div , 0th index is ignored([1:]) because it will be parent div with all the children div in it
    for el in _list:
        print(el.text)
