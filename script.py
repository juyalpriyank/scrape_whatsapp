from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

already_scraped = {}


def launch_browser():
    """ later make just one function and use sleep so that browser will not keep shutting down"""
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get('https://web.whatsapp.com')

async def start_scrape(scroll=0):
    """ This is a test function which will contain the possible scraping ways"""
    target = driver.find_element_by_id('pane-side')
    driver.execute_script(f"arguments[0].scrollTop = {scroll}", target)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    a = soup.findAll("div", {"id": "pane-side"})[0] #This will fetch all the left side panel's code
    soup = BeautifulSoup(str(a), 'lxml')
    _list = soup.findAll('div', {'tabindex' : '-1'})[1:] #This _list will contain all the chats div , 0th index is ignored([1:]) because it will be parent div with all the children div in it
    for el in _list:
        text = el.find('span', {'title': True})['title']
        if text not in already_scraped.keys():
            driver.find_element_by_xpath(f"//span[text()='{text}']").click()
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
            already_scraped.update({text: True})
            c = await reload_soup(driver)
            while await print_to_console(driver, c):
                print('pass')
                c = await reload_soup(driver)
        break
    scroll += 350
    start_scrape(scroll)

async def print_to_console(driver, c):
    try:
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@title,'load earlier messages…')]")))
        driver.find_element_by_xpath("//div[contains(@title,'load earlier messages…')]").location_once_scrolled_into_view
        return True

    except Exception as e:
        c = await reload_soup(driver)
        print(e)
        for l in c:
            print(l.text)
        return False


async def reload_soup(driver):
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    a = soup.find('div', {"id" : "main"})
    soup = BeautifulSoup(str(a), 'lxml')
    b = soup.find('div', {"class" : "copyable-area"})
    b = list(b)
    b= b[2]
    soup = BeautifulSoup(str(b), 'lxml')
    c = soup.findAll('div',{"class" : "copyable-text"})     #This has all divs for each message which has information if the message is replied to or normal message
    return c

"""
code for chat window
source = driver.page_source
soup = BeautifulSoup(source, 'lxml')
a = soup.find('div', {"id" : "main"})
soup = BeautifulSoup(str(a), 'lxml')
b = soup.find('div', {"class" : "copyable-area"})
b = list(b)
b= b[2]
soup = BeautifulSoup(str(b), 'lxml')
c = soup.findAll('div',{"class" : "copyable-text"})     #This has all divs for each message which has information if the message is replied to or normal message

for l in c:
    print(l.text)

driver.find_element_by_xpath("//div[contains(@title,'load earlier messages…')]").location_once_scrolled_into_view                      #Scrolls/ calls the loader of the chat window for new messages

"""



if __name__ == '__main__':
    launch_browser()
