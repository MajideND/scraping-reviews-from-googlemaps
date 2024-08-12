import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from openpyxl import Workbook
import pandas as pd

from env import URL, DriverLocation

def get_data(driver, dataStructreType):
    """
    this function get main text, score, name
    """
    print('get data...')
    more_elemets = driver.find_elements_by_class_name('w8nwRe kyuRq')
    for list_more_element in more_elemets:
        list_more_element.click()
    if dataStructreType == 1:
        elements = driver.find_element_by_xpath('//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[9]')
    else:
        elements = driver.find_element_by_xpath('//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[8]')
    childElement = elements.find_element_by_xpath('.//div[1]')
    childElementClassName = childElement.get_attribute('class')
    elements = elements.find_elements_by_xpath(f'//*[@class="{childElementClassName}"]')
    
    childElementNameClass = childElement.find_element_by_xpath('.//div[1]/div[1]/div[2]/div[2]/div[1]/button[1]/div[1]').get_attribute('class')
    childElementTextClass = childElement.find_element_by_xpath('.//div[1]/div[4]/div[2]/div[1]/span[1]').get_attribute('class')
    childElementScoreClass = childElement.find_element_by_xpath('.//div[1]/div[1]/div[4]/div[1]/span[1]').get_attribute('class')
    lst_data = []
    for data in elements:
        name = 'No name'
        text = 'No text'
        score = '-'
        try:
            name = data.find_element_by_xpath(
                f'.//*[@class="{childElementNameClass}"]').text
            score = data.find_element_by_xpath(
                f'.//*[@class="{childElementScoreClass}"]').get_attribute("aria-label")
            text = data.find_element_by_xpath(
                f'.//*[@class="{childElementTextClass}"]').text

        except:
            pass
        
        lst_data.append([name + " from GoogleMaps", text, score[0]])

    return lst_data

def ifGDRPNotice(driver):
    # check if the domain of the url is consent.google.com
    if 'consent.google.com' in driver.current_url:
        # click on the "I agree" button
        driver.execute_script('document.getElementsByTagName("form")[0].submit()');
    return

def ifPageIsFullyLoaded(driver):
    # check if the page fully loaded including js
    return driver.execute_script('return document.readyState') != 'complete'

def counter():
    dataStructreType = 1
    try:
        result = driver.find_element_by_xpath('//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]').find_element_by_class_name('fontBodySmall').text
    except:
        dataStructreType = 2
        result = driver.find_element_by_xpath('//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]').find_element_by_class_name('fontBodySmall').text
    result = result.replace(',', '')
    result = result.replace('.', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(int(result[0])/10)+1, dataStructreType


def scrolling(counter):
    print('scrolling...')
    scrollable_div = driver.find_element_by_xpath(
        '//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[last()]')
    for _i in range(counter):
        
        scrolling = driver.execute_script(
            """
            var xpathResult = document.evaluate('//body/div[2]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            var element = xpathResult.singleNodeValue;
            element.scrollTop = element.scrollHeight;
            """,
            scrollable_div
        )
        time.sleep(3)


def write_to_xlsx(data):
    print('write to excel...')
    cols = ["name", "comment", 'rating']
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('out.xlsx')


if __name__ == "__main__":

    print('starting...')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # show browser or not
    options.add_argument("--lang=en-US")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    DriverPath = DriverLocation
    driver = webdriver.Chrome(DriverPath, options=options)

    driver.get(URL)
    
    while ifPageIsFullyLoaded(driver):
        time.sleep(1)
        
    ifGDRPNotice(driver)
    
    while ifPageIsFullyLoaded(driver):
        time.sleep(1)

    counter = counter()
    scrolling(counter[0])

    data = get_data(driver, counter[1])
    driver.close()

    write_to_xlsx(data)
    print('Done!')
