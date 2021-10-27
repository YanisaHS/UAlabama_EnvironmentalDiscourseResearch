# This file will open the links I already got and extract the article info I want

import time, random
from bs4 import BeautifulSoup as bsoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from Classes.saveBristolBayArticleInformation import SaveBristolBayArticleInformation

# Create function to make random sleep intervals (rather than always 2 seconds)
def randomSleepsFunction():
    return random.randrange(10, 40, 1) / 10.0 #0.1 is step size - so it can randomize 1.1, 1.2, 1.3, ... 3.9, 4.0 etc.

# Start with running chrome driver with Selenium:
chromeDriverPath = '/Users/yanisa/Code_GitHub/2020_ResearchAssistant_UA_EnvironmentalDiscourse/chromedriver'

chromeOptions = Options()
chromeOptions.add_argument('--headless')
webDriver = webdriver.Chrome(executable_path=chromeDriverPath, options=chromeOptions)

# Open the file of saved links and put the links in a list to loop over later
links = open('saveBristolBay_ArticleLinks.txt').read()
listOfLinks = links.split('\n')

# Open each link and get the articles
articleNumber = 1 # to get it started
listOfEachArticleInfo = []
with webDriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 20)
    driver.implicitly_wait(30)
    driver.maximize_window()

    for eachURL in listOfLinks:
        print('Opening article #' + str(articleNumber))
        driver.get(eachURL)

        # Get html to be parsed by bsoup
        time.sleep(randomSleepsFunction())
        # Protect against timeout errors/pages that don't work for some reason
        retries = 0
        while retries < 2:
            try:
                wait.until(presence_of_element_located((By.CLASS_NAME, "entry-title")))
                break
            except TimeoutException:
                driver.refresh()
                retries = retries + 1
                print('Retry #' + str(retries))
        if retries == 2: # if it tried and STILL doesn't work, just skip it and keep going
            print('URL skipped - retries exceeded ' + eachURL)
            exit()
        html = driver.execute_script("return document.documentElement.outerHTML;")

        # Use bsoup to extract info from html
        soup = bsoup(html, 'html.parser')

        # Wrapping in try/except in case some page randomly doesn't match the template
        try:
            # Headline
            inProcessHeadline = soup.find('div', attrs={'class': 'post-title'})
            if inProcessHeadline != None:
                headline = inProcessHeadline.text
            else:
                inProcessHeadline = soup.find('h1', attrs={'class': 'entry-title'})
                headline = inProcessHeadline.text

            # Organization
            organization = 'Save Bristol Bay'

            # Date
            inProcessDate = soup.find('time')
            date = inProcessDate.text

            # URL
            url = eachURL

            # Text
            text = ''
            inProcessText = soup.find('div', attrs={'class': 'entry-content'})
            inProcessTextSecond = inProcessText.find_all('p')
            for paragraph in inProcessTextSecond:
                text = text + ' ' + paragraph.text
                
            # Put things in class, save info, increment article count
            putThingsInClass = SaveBristolBayArticleInformation(headline, organization, date, url, text)
            listOfEachArticleInfo.append(putThingsInClass)
            articleNumber = articleNumber + 1
        except Exception as exception:
            print('URL skipped - page doesn\'t match template: ' + eachURL)
            print(exception)

    # must close the driver after task finished
    driver.close()

# Save to individual .txt files
beginningFilePath = '/Users/yanisa/GoogleDrive/Data_Research/RA_Fall2020_UAlabama/scrapedArticles/saveBristolBay/'
for article in listOfEachArticleInfo:
    makeFile = open(beginningFilePath + article.date + '_' + article.headline + '.txt', 'w')
    makeFile.write(article.headline + '\n' + article.organization + '\n' + article.date + '\n' + \
        article.url + '\n\n' + article.text)
print('QUEEN NISSY IS DONE!!!!! <3')