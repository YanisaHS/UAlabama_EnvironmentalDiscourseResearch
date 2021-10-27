# This file will parse through the articles and look for ones which have the following keywords:
#   Adani or Carmichael

import os

origDataFilePath = '/Users/yanisa/GoogleDrive/Data_Research/RA_Fall2020_UAlabama/scrapedArticles/lockTheGate/AllArticles/'
# TODO change final data path as necessary - which keywords folder at end
finalDataFilePath = '/Users/yanisa/GoogleDrive/Data_Research/RA_Fall2020_UAlabama/scrapedArticles/lockTheGate/Keywords_adani_OR_carmichael/'

origDataFile = os.listdir(origDataFilePath)
for eachFile in origDataFile:
    # Opening file - if any characters program can't recognize, will just save them (w/o reading) and copy them back in at the end
    openedFile = open(origDataFilePath + eachFile, errors="surrogateescape")
    readFile = openedFile.read()
    lowerArticle = readFile.lower()
    # If keywords in file, write the file into the correct folder
    if 'adani' in lowerArticle or 'carmichael' in lowerArticle:
        newFile = open(finalDataFilePath + eachFile, 'w')
        newFile.write(readFile)
print('Done!!!! :)')
