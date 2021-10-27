import pandas as pd

version = '2'
inputCSVFilePath = '/Users/yanisa/Code_GitHub/2020-2021_ResearchAssistant_UA_EnvironmentalDiscourse/randomOtherScripts/EnvOrgs_GIS_Data{}.csv'.format(version)

#Load the CSV into a dataframe
df = pd.read_csv(inputCSVFilePath, encoding = 'UTF-8')

# Repeat rows based on the freq column
df = df.loc[df.index.repeat(df['Freq'])]

print(df)

# Export to .csv
df.to_csv('/Users/yanisa/Code_GitHub/2020-2021_ResearchAssistant_UA_EnvironmentalDiscourse/randomOtherScripts/EnvOrgs_GIS_EditedData{}.csv'.format(version), index = None, sep = ',')