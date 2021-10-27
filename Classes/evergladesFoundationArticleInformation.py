from datetime import datetime

class EvergladesFoundationArticleInformation():

    # Making article info objects
    def __init__(self, headline, organization, date, url, text):
        self.headline = self.headlineCleaning(headline.strip())
        self.organization = organization
        self.date = self.dateCleaning(date)
        self.url = url
        self.text = text
    
    # Clean date since it will output into the file name as well
    def dateCleaning(self, date):
        incomingFormatBefore2020 = '%b %d, %Y'
        incomingFormat2020 = '%b %d'
        if ',' in date:
            makeOrigInDateTimeObj_Before2020 = datetime.strptime(date.strip(), incomingFormatBefore2020)
            outgoingFormat_Before2020 = '%Y_%m_%d'
            finalDate = makeOrigInDateTimeObj_Before2020.strftime(outgoingFormat_Before2020)
        if ',' not in date:
            makeOrigInDateTimeObj_2020 = datetime.strptime(date.strip(), incomingFormat2020)
            outgoingFormat_2020 = '2020_%m_%d'
            finalDate = makeOrigInDateTimeObj_2020.strftime(outgoingFormat_2020)
        return finalDate

    # remove / char from headline
    def headlineCleaning(self, headline):
        finalHeadline = headline.replace('/', '-')
        return finalHeadline