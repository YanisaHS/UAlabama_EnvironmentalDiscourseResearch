class SaveBristolBayArticleInformation():

    # Making article info objects
    def __init__(self, headline, organization, date, url, text):
        self.headline = headline.strip()
        self.organization = organization
        self.date = self.dateCleaning(date)
        self.url = url
        self.text = text

    # Clean date since it will output into the file name as well
    # Remove commas and make spaces '_'
    def dateCleaning(self, date):
        finalDate = date.replace(',', '').replace(' ', '_')
        return finalDate

        