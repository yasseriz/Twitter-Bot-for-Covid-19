# Import Libraries
import tweepy
import sys
import requests
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from bs4 import BeautifulSoup
from datetime import datetime

# Authentication to Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Creating an API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print('Authentication Successful')
except:
    print('Error while authenticating API')
    sys.exit(1)

response = requests.get('https://www.worldometers.info/coronavirus/country/malaysia/')
soup = BeautifulSoup(response.content, 'lxml')

# Obtaining daily data
dateToday = datetime.today().strftime('%d %b %Y')
daily = soup.find("li", {"class":"news_li"}).findAll("strong")
source = soup.find("li", {"class":"news_li"}).find("a", {"class":"news_source_a"})

cases = [detail.get_text() for detail in daily]

# Obtaining total data
numbers = soup.findAll("div", {"class": "maincounter-number"})
data = []
dataName = ['Total Cases', 'Deaths', 'Recovered']
for i in numbers:
    data.append(i.get_text().strip())

newData = dict(zip(dataName, data))

# Tweet
tweet = f'''Coronavirus Latest Updates - Malaysia

Daily Cases - {dateToday}

{cases[0]}
{cases[1]}
Source: {source["href"]}

Total cases:{newData['Total Cases']} 
Recovered:{newData['Recovered']} 
Deaths:{newData['Deaths']} 
Source: https://www.worldometers.info/coronavirus/

#coronavirus #covid19 #coronavirusupdates
'''

api.update_status(tweet)
print('Tweet Successful')