import random, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup as bsoup

# Create function to make random sleep intervals (rather than always 2 seconds)
def randomSleepsFunction():
    return random.randrange(10, 40, 1) / 10.0 #0.1 is step size - so it can randomize 1.1, 1.2, 1.3, ... 3.9, 4.0 etc.

# Not using referer because selenium doesn't have that built in
# Also doesn't really matter, since I am clicking the 'next page' button, so my referers are correct

# Start with running chrome driver with Selenium:
chromeDriverPath = '/Users/yanisa/Code_GitHub/2020_ResearchAssistant_UA_EnvironmentalDiscourse/chromedriver'

chromeOptions = Options()
chromeOptions.add_argument('--headless')
webDriver = webdriver.Chrome(executable_path=chromeDriverPath, options=chromeOptions)

# Go to the main url and start saving all the urls to a list (to be printed later)
finalListOfArticleURLs = []
pageNumber = 2 # to get it started - will increment below
url = 'https://www.grandcanyontrust.org/blog'
with webDriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 20)
    driver.implicitly_wait(30)
    driver.maximize_window()

    # Open the url
    print('Opening url...')
    driver.get(url)

    while True:
        # Get html to be parsed by bsoup
        time.sleep(randomSleepsFunction())
        # Protect against timeout errors/pages that don't work for some reason
        retries = 0
        while retries < 2:
            try:
                wait.until(presence_of_element_located((By.CLASS_NAME, "title")))
                break
            except TimeoutException:
                driver.refresh()
                retries = retries + 1
                print('Retry #' + str(retries))
        if retries == 2: # if it tried and STILL doesn't work, just skip it and keep going
            print('URL skipped - retries exceeded ' + eachURL)
            exit()
        html = driver.execute_script("return document.documentElement.outerHTML;")

        # Use bsoup to get each article link and save them to a list
        soup = bsoup(html, 'html.parser')
        allURLs = soup.find_all('div', attrs={'class': 'title'})
        try:
            for eachURL in allURLs:
                articleURLFirst = eachURL.find('a', href=True)
                articleURL = articleURLFirst['href']
                finalListOfArticleURLs.append(articleURL)
        except Exception as exception:
            print('URL skipped - caused exception: ' + articleURL)
            print(exception)

        # Click "Older Posts" button if it exists
        try:
            olderPostsButton = soup.find('li', attrs={'class': 'next'})
            olderPostsButtonPageURLFirst = olderPostsButton.find('a', href=True)
            olderPostsButtonPageURL = olderPostsButtonPageURLFirst['href']
            print(olderPostsButtonPageURL)
            driver.get('https://www.grandcanyontrust.org' + olderPostsButtonPageURL)
        except:
            break

# Write list of links to a file:
fileToWrite = open('grandCanyonTrust_ArticleLinks.txt', 'w')
for eachLink in finalListOfArticleURLs:
    # write each link to a new line
    fileToWrite.write('https://www.grandcanyontrust.org' + eachLink)
    fileToWrite.write('\n')
fileToWrite.close()