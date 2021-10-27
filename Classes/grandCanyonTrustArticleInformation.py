class GrandCanyonTrustArticleInformation():

    # Making article info objects
    def __init__(self, headline, organization, date, url, text):
        self.headline = self.headlineCleaning(headline.strip())
        self.organization = organization
        self.date = self.dateCleaning(date.strip())
        self.url = url
        self.text = text
    
    # Clean date since it will output into the file name as well
    # Remove commas and make spaces '_'
    def dateCleaning(self, date):
        finalDate = date.replace(u'\xa0', '_').replace(' ', '_')
        return finalDate

    # remove / char from headline
    def headlineCleaning(self, headline):
        finalHeadline = headline.replace('/', '-')
        return finalHeadline