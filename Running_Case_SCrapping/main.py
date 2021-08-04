#STEP 1 : install al the reqirements  by the command 'pip install -r requirements.txt'
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://www.hubertiming.com/results/2017GPTR10K"

#STEP 2 : get the content 
r = requests.get(url)
htmlContent = r.content
#htmlContent = urlopen(url)


#STEP 3 : Parse the HTML
soup = BeautifulSoup(htmlContent , 'html.parser')
#print(soup.prettify) # show the content clearly

#STEP 4 : HTML Tree
#commonly used types of object
# 1 - tag
# 2 - Navigable string
# 3- Beautiful soup
#4 - Comment
title = soup.title
#print(title)
# print(type(soup))
# print(type(title.string))

# Print out the text
text = soup.get_text()
#print(text)
#print(soup.text)

A = soup.find_all('a')
#print(A)

#to get all the link in the anchor tag

# all_link = soup.find_all('a')
# for link in all_link:
#     print(link.get('href'))

#to get the tbale rows 


table_row = soup.find_all('tr')
#print(table_row[:10])

#to get all rows of the data
for row in table_row:
    row_td = row.find_all('td')
    #print(row_td)

string = str(row_td)
cleaning = BeautifulSoup(string , 'html.parser').get_text()
#print(cleaning)

#generates an empty list, extract text in between html tags for each row, and append it to the assigned list.
import re 

list_rows = []
for row in table_row:
    cells = row.find_all('td')
    str_row = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean , '' , str_row))
    list_rows.append(clean2)

#print(clean2)

#converting to pandas dataframe
import pandas as pd 
data = pd.DataFrame(list_rows)
#print(data.columns)

data1 = data[0].str.split(',' , expand =True)
#print(data1[0])
data1[0] =  data1[0].str.split('[')
data1 = data[0].str.split(',' , expand =True)
#print(data1.head(10))
#print(data1.head(10))

#for COlumns names
col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "html.parser").get_text()
all_header.append(cleantext2)
#print(all_header)

df2 = pd.DataFrame(all_header)
#print(df2.head())

df3 = df2[0].str.split(',', expand=True)
#print(df3.head())

#combine COlumns name and data
frames = [df3, data1]

df4 = pd.concat(frames)
#print(df4.head(10))

df5 = df4.rename(columns=df4.iloc[0])
#print(df5.head())

df6 = df5.dropna(axis=0, how='any')
df7 = df6.drop(df6.index[0])
#print(df7.head())

#Data Modification 

df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)
#print(df7.head())


df7['Place'] = df7['Place'].str.strip('[').astype(int)
df7['Team'] = df7['Team'].str.strip(']').astype(str)
print(df7.columns)
#print(type(df7[' Name'].iloc[0]))
df7[' Name'] = [x.replace("\r\n","") for x in df7[' Name']]
df7[' Name'] = df7[' Name'].str.strip()

df7['Team'] = [x.replace("\r\n","") for x in df7['Team']]
df7['Team'] = df7['Team'].str.strip()

print(df7.columns)

#save data into csv format
df7.to_csv('Runner_Data.csv')
print(df7.head())



