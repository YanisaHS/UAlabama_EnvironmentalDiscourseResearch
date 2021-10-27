# This doc will be to download Environmental Impact Statements (EIS) from the EPA website:
#   https://cdxnodengn.epa.gov/cdx-enepa-public/action/eis/search
# This will be used to download documents by keyword and timeframe
# Documents will be downloaded into Drive, but then later moved to Box since they are very large

# https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search/search
# EIS webiste is set up so it sends a form to this ^^ url with the search criteria
#   grabbed url by doing dev tools -> Network -> copied link from "search" (& opened "search" to get the form parameters)
#   look at "Form Data" section at the bottom of that search to see what they name their parameters/send in form/etc

import requests, random, time, shutil
from bs4 import BeautifulSoup as bsoup

# Variables which change based on search criteria:
searchKeyword = 'mine'
startDate = '02/01/2011'
endDate = '02/07/2021'
pageNumber = 2 # to get it started - used only at the very bottom

url = 'https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search/search'

# Create function to make random sleep intervals (rather than always 2 seconds)
def randomSleepsFunction():
    return random.randrange(10, 40, 1) / 10.0 #0.1 is step size - so it can randomize 1.1, 1.2, 1.3, ... 3.9, 4.0 etc.

# Setting up form things to post to html
valuesToSend = {'searchCriteria.title' : searchKeyword,
                'searchCriteria.startFRDate' : startDate,
                'searchCriteria.endFRDate' : endDate,
                'searchRecords' : 'Search'}

# create a session so it saves all my search info and sends it even when i switch pages/etc
session = requests.Session()
postData = session.post(url, data=valuesToSend)

### BELOW IS ONLY FOR TESTING - write it to a html file so i can look at it in chrome ###
# openFakeFile = open('test.html', 'w')
# openFakeFile.write(postData.text)
# openFakeFile.close()

firstSoup = bsoup(postData.text, 'html.parser')

while True:
    # Next - will have to use bsoup to look at the html to download each final draft pdf to a certain file
    # Put it into the html for bsoup to look through
    # website has each row in 'even' or 'odd' classes for some reason for each table row - both are tr class
    allRows = firstSoup.find_all('tr')
    for eachRow in allRows:
        time.sleep(randomSleepsFunction())
        eachRowItem = eachRow.find_all('td')
        if len(eachRowItem) < 2:
            continue
        # index in so I can get the specific 'td' - see if it says 'Final' (ie. it's not a 'draft')
        #   also have to get proj name and date so I can name the files
        documentStatus = eachRowItem[1]
        if 'Final' in str(documentStatus):
            time.sleep(randomSleepsFunction())
            print('Found doc...')
            # Get project name
            projNameFirst = eachRowItem[0].text
            projName = projNameFirst.replace('\n','').replace(' ', '')
            print(projName)

            # Get date
            dateFirst = eachRowItem[3].text
            dateNoNewLine = dateFirst.replace('\n','')
            dateParts = dateNoNewLine.split('/')
            year = dateParts[2]
            day = dateParts[1]
            month = dateParts[0]
            date = year + '_' + month + '_' + day
            print(date)

            downloadBoxCommentsAndDoc = eachRowItem[6]
            # index it again to just get the EIS letter, not the comment letter
            eisLetter = downloadBoxCommentsAndDoc.find_all('a')[0]
            urlToDownloadDoc = eisLetter.get('href')

            # Use requests to actually get the doc for real
            fullURL = 'https://cdxnodengn.epa.gov' + urlToDownloadDoc
            # Download the doc and put it back together to save it in my file
            filepathToSaveDocTo = '/Users/yanisa/Desktop/eisDocs/' + date + '_' + projName
            # stream=True just means that it will write while it reads along rather than
            #   waiting until it has everything
            print('Writing doc...')
            with requests.get(fullURL, stream=True) as getDocument:
                # make it save in the same extension (.pdf or .zip) as orig
                #   'content-type' i got from dev tools -> network -> response headers -> 'content-type'
                fileType = getDocument.headers['content-type']
                if 'zip' in fileType:
                    extension = '.zip'
                elif 'pdf' in fileType:
                    extension = '.pdf'
                else:
                    print(fullURL)
                    continue
                # Add extension to filepath
                filepathToSaveDocTo = filepathToSaveDocTo + extension
                # 'wb' stands for 'write binary' (instead of text) - need this because it's a pdf
                with open(filepathToSaveDocTo, 'wb') as makeDocument:
                    shutil.copyfileobj(getDocument.raw, makeDocument)
                    time.sleep(randomSleepsFunction())
    
    # Have it click 'next' if there is a next page
    pageLinksButton = firstSoup.find_all('span', attrs={'class': 'pagelinks'})
    bottomPageLinksButton = pageLinksButton[1]
    # find the one that = 'Next' (not contains) and open its href
    getAllHREFs = bottomPageLinksButton.find_all('a')
    # set firstSoup to be 'None' - if it's still 'none' at the end, then end program
    firstSoup = None
    for eachAClass in getAllHREFs:
        if eachAClass.text == 'Next':
            # May have to change session id?
            baseURLForNextPage = 'https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search/search'
            print('Going to page #' + str(pageNumber))
            # Have to give the parameters again
            valuesToSend = {'searchCriteria.title' : searchKeyword,
                            'searchCriteria.startFRDate' : startDate,
                            'searchCriteria.endFRDate' : endDate,
                            'searchRecords' : 'Search',
                            'd-446779-p': pageNumber}
            html = session.get(baseURLForNextPage, params=valuesToSend)
            print('Going to: ' + str(html.url))
            firstSoup = bsoup(html.text, 'html.parser')
            pageNumber = pageNumber + 1
    if firstSoup == None:
        exit() 



