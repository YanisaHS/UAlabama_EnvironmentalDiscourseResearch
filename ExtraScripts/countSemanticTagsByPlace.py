# This file will keep track of the semantic tags that take place around each place name
# Semantic tags will be counted that are on the place name word or any words 4 to the left or right
# Not skipping over punctuation

# What it basically is going to do is take a place name (from input file), then find that place name in the tagged text,
#   then once it finds one, go through each semantic tag one by one for the place names plus the 4 words to the left and right,
#   and increment for each tag it finds that matches one of the semantic tags. This way, I can ignore the extra stuff
#   (e.g. '+' or '[i36]' or w/e)
# Then put it back into a .csv file to be read by excel

import pandas as pd

# If doing all orgs together, keep below line - this is the orig one
#inputCSVFilePath = 'inputDataFrameEmpty_SemanticTagCounting_upperAndlowerCase.csv'

# If doing by each separate org, use below lines, but change based on organization name
### NOTE: HAVE TO CHANGE INPUT DATA FRAME ### - make sure it matches file format of ^^inputCSVFilePath - use _
organization = 'rmt'
inputCSVFilePath = './jan2021Update_textFiles_OutputFiles_ByOrganization/{}_inputDataFrame.csv'.format(organization)

# Load my .csv empty table in as a dataframe
#   index_col=0 is so it takes the first row AND column as labels, not just the first row (and leaving the first column as normal data)
df = pd.read_csv(inputCSVFilePath, encoding = 'UTF-8', index_col=0)
#print(df.head(5))
#print(df.at[8, 'A1.6'])

# Sample input text - will upload file later
# inputText = '''As_Z5 an_Z5 environmental_W5 educator_P1/S2mf with_Z5 the_Z5 
# Chesapeake_Z2[i14.2.1 Bay_Z2[i14.2.2 Foundation_T2+ ,_PUNC I_Z8mf have_Z5 
# retained_A9+ my_Z8 love_S3.2 of_Z5 nature_W5 ._PUNC 
# Now_T1.1.2 ,_PUNC I_Z8mf \'m_Z5 trying_X8+ to_Z5 reconnect_Z99 with_Z5 that_Z5 
# budding_X7+ artist_C1/S2mf and_Z5 bring_M2/N6+[i15.2.1 back_M2/N6+[i15.2.2 
# the_Z5 awe_E1 and_Z5 wonder_X2.1 I_Z8mf remember_X2.2+ feeling_X2.1 about_Z5 
# the_Z5 natural_A6.2+ world_W1 as_Z5 a_Z5 child_S2mf/T3- ._PUNC 
# In_Z5 next_T1.1.3[i16.2.1 summer_T1.1.3[i16.2.2 \'s_Z5 Chesapeake_Z99 
# Classrooms_P1/H2 Art_C1 &;_PUNC Environmental_W5 Literacy_Q1.2/P1[i17.2.1 
# course_Q1.2/P1[i17.2.2 ,_PUNC I_Z8mf \'ll_T1.1.3 be_A3+ challenging_A12- 
# teachers_P1/I3.2/S2mf from_Z5 Anne_Z1mf[i18.2.1 Arundel_Z1mf[i18.2.2 County_M7 
# to_Z5 do_A1.1.1 the_Z5 same_A6.1+++ ._PUNC'''.replace('\n', '')

# if doing all orgs together, keep below line
#inputText = open('ALL_ORGS_CAT_TAGGED_taggedTextInput.txt').read()

# if doing organizations separately, keep below lines, but change org name (above)
inputText = open('./jan2021Update_textFiles_OutputFiles_ByOrganization/{}_Text.txt'.format(organization)).read()

placeNamesFullList = list(df.index)
semanticTagsList = list(df.columns.values)

for placeName in placeNamesFullList:
    print('Next place name...')
    # Lower it and split on _ for multi-word place names
    placeNameLower = placeName.lower().split('_')
    # Index the text so I can check the words 4 +/- and get those tags too
    inputTextList = inputText.lower().split(' ')
    for eachWordToBeIndexed in range(0, len(inputTextList)):
        actualWordText = inputTextList[eachWordToBeIndexed]
        # Now check if the place name is in the text
        if placeNameLower[0] in actualWordText:
            # hard-coding the chesapeake situation - chesapeake bay OR chesapeake are accepted
            #   if 'chesapeake' is found under 'chesapeake' (only, not bay) line, then ignore it if the next word is bay
            #   if len(placeNameLower) == 1 then I'm just on the chesapeake (not CB) line
            if placeNameLower[0] == 'chesapeake' \
            and len(placeNameLower) == 1 \
            and 'bay' in inputTextList[eachWordToBeIndexed + 1]:
                continue
            # Setting this as True to use later
            placeAndTextWordsMatch = True
            # if len > 1 (e.g. Grand Canyon National Park), then have to check to make sure all the words match in order
            # if len = 1 (e.g. Chicago), don't have to do anything special (no elif)
            if len(placeNameLower) > 1:
                for eachWordIndexFromPlaceName in range(0, len(placeNameLower)):
                    eachWordTextFromPlaceName = placeNameLower[eachWordIndexFromPlaceName]
                    # Check to see if the word from the place name DO NOT MATCH the word from the input text
                    #   if they don't match, then they aren't a match (e.g. 'Grand Canyon National Land' would mark to False)
                    #   then break out of loop
                    if eachWordTextFromPlaceName not in inputTextList[eachWordToBeIndexed + eachWordIndexFromPlaceName]:
                        placeAndTextWordsMatch = False
                        break
            # if any of False matches were hit, then it isn't a match, so just keep reading along
            if placeAndTextWordsMatch == False:
                continue
            # if it's True, then it's a match, so I need to get the tags for that word + the 4 left & 4 right tags
            if placeAndTextWordsMatch == True:
                placeNamePlusFourLeftAndRightList = []
                # grab the chunk of text that includes the place name and 4 left and right (3 variables: placeName, left, right)
                # first, get the place name index (of the last word), then calculate the left and right
                placeNameIndexLastWord = eachWordToBeIndexed + len(placeNameLower) - 1
                placeNameText = inputTextList[eachWordToBeIndexed:placeNameIndexLastWord]
                # Adding place name here - so technically it will be out of order
                #   i.e. the final list is: place name, left words, right words (can fix later if necessary)
                # .extend() because it's a list
                placeNamePlusFourLeftAndRightList.extend(placeNameText)
                for leftWordsIndex in range ((eachWordToBeIndexed - 4), eachWordToBeIndexed):
                    leftWordsText = inputTextList[leftWordsIndex]
                    placeNamePlusFourLeftAndRightList.append(leftWordsText)
                for rightWordsIndex in range (placeNameIndexLastWord, (placeNameIndexLastWord + 5)):
                    rightWordsText = inputTextList[rightWordsIndex]
                    placeNamePlusFourLeftAndRightList.append(rightWordsText)
                
                # Now that I have the whole chunk I want to get the tags from, can count the semantic tags
                for eachElement in placeNamePlusFourLeftAndRightList:
                    # will add all elements to this list after their cleaned, then check the list & count tags
                    listOfWordsAndCleanedTags = []
                    # Remove the +/- characters and split on _, which is what separates the word from the tags
                    splitEachSemanticTagAndRemoveChars = eachElement.replace('+', '').replace('-', '').replace('m', '').replace('f', '').replace('n', '').replace('c', '').split('_')
                    for eachSplitElement in splitEachSemanticTagAndRemoveChars:
                        # Split on /, which is the char used to split multiple semantic tags
                        #   (will only be present in ones which have more than one semantic tag)
                        splitAgainInCaseOfMultipleTags = eachSplitElement.split('/')
                        # Remove any '[i306.1.1' (or w/e) - these are not consistent numbers, but some tags have this
                        #   thing at the end - it always starts w/ a '[' though and goes until the end of the element
                        for eachSplitElementSecond in splitAgainInCaseOfMultipleTags:
                            if '[' in eachSplitElementSecond:
                                bracketIndex = eachSplitElementSecond.index('[')
                                cleanedTag = eachSplitElementSecond[:bracketIndex]
                                listOfWordsAndCleanedTags.append(cleanedTag)
                            else:
                                listOfWordsAndCleanedTags.append(eachSplitElementSecond)
                    # Now compare to the official tags list to my cleaned list
                    for eachWordOrCleanedTag in listOfWordsAndCleanedTags:
                        for eachSemanticTag in semanticTagsList:
                            lowerEachSemanticTag = eachSemanticTag.lower()
                            # If a semantic EQUALS (not in) the word/tag, then increment
                            if lowerEachSemanticTag == eachWordOrCleanedTag:
                                eachSemanticTagCount = df.at[placeName, eachSemanticTag]
                                updatedSemanticTagCount = eachSemanticTagCount + 1
                                # Now that it's been incremented +1, re-assign it to the same location/cell
                                df.at[placeName, eachSemanticTag] = updatedSemanticTagCount

# Export to .csv
# if doing all orgs in one, keep below line
#df.to_csv("outputDataFrame_SemanticTagCounting.csv")#, index = None, sep = ',')

# if doing different orgs separately, keep below line, but change org (above)
df.to_csv('./jan2021Update_textFiles_OutputFiles_ByOrganization/{}_outputDataFrame_SemanticTagCounting.csv'.format(organization))


# TODO After running code, will have to deal with the 'Chesapeake Bay' thing:
#   manually add all of the 'Chesapeake Bay' results to 'Chesapeake'
#   since poole wants CD or just C