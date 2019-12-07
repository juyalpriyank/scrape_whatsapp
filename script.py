from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

already_scraped = {}            #A hash to keep track of all the chats that have been already scraped by the script

#launches browser
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
driver = webdriver.Chrome("--driver_path", options=options)         #Give the path of your chrome driver
driver.get('https://web.whatsapp.com')

async def start_scrape(scroll=0):
    """ This is a test function which will contain the possible scraping ways"""
    target = driver.find_element_by_id('pane-side')
    driver.execute_script(f"arguments[0].scrollTop = {scroll}", target)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    left_panel = soup.findAll("div", {"id": "pane-side"})[0] #This will fetch all the left side panel's code
    left_panel_soup = BeautifulSoup(str(left_panel), 'lxml')
    chat_div_list = left_panel_soup.findAll('div', {'tabindex' : '-1'})[1:] #This _list will contain all the chats div , 0th index is ignored([1:]) because it will be parent div with all the children div in it
    for chat_div in chat_div_list:
        chat_name = chat_div.find('span', {'title': True})['title']
        if chat_name not in already_scraped.keys():
            driver.find_element_by_xpath(f"//span[text()='{chat_name}']").click()
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
            already_scraped.update({chat_name: True})
            reloaded_soup = await reload_soup(driver)
            while await print_to_console(driver, reloaded_soup):
                print('processing...')
                reloaded_soup = await reload_soup(driver)
    scroll += 350
    start_scrape(scroll)

async def print_to_console(driver, c):
    try:
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@title,'load earlier messages…')]")))
        driver.find_element_by_xpath("//div[contains(@title,'load earlier messages…')]").location_once_scrolled_into_view
        return True

    except Exception as e:
        reloaded_soup = await reload_soup(driver)
        print(e)
        for text_div in reloaded_soup:
            print(text_div.text)
        print('\n \n \n Scrapping next chat.......')
        return False


async def reload_soup(driver):
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    all_soup = soup.find('div', {"id" : "main"})
    soup = BeautifulSoup(str(all_soup), 'lxml')
    filtered_soup = soup.find('div', {"class" : "copyable-area"})
    filtered_soup = list(filtered_soup)[2]
    soup = BeautifulSoup(str(filtered_soup), 'lxml')
    final_soup = soup.findAll('div',{"class" : "copyable-text"})     #This has all divs for each message which has information if the message is replied to or normal message
    return final_soup


if __name__ == '__main__':
    launch_browser()
