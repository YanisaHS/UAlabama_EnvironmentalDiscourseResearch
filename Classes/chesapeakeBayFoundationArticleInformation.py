from datetime import datetime

class ChesapeakeBayFoundationArticleInformation():

    # Making article info objects
    def __init__(self, headline, organization, date, url, text):
        self.headline = self.headlineCleaning(headline.strip())
        self.organization = organization
        self.date = self.dateCleaning(date)
        self.url = url
        self.text = text
    
    # Clean date since it will output into the file name as well
    def dateCleaning(self, date):
        incomingFormat = '%d %b %Y'
        makeOrigInDateTimeObj = datetime.strptime(date.strip(), incomingFormat)
        outgoingFormat = '%Y_%m_%d'
        finalDate = makeOrigInDateTimeObj.strftime(outgoingFormat)
        return finalDate

    # remove / char from headline
    def headlineCleaning(self, headline):
        finalHeadline = headline.replace('/', '-')
        return finalHeadline