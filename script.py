from bs4 import BeautifulSoup
from selenium import webdriver

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
            already_scrape.update({text: True})
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

            driver.find_element_by_xpath("//div[contains(@title,'load earlier messages…')]").location_once_scrolled_into_view
            break

    scroll += 350
    start_scrape(scroll)

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
