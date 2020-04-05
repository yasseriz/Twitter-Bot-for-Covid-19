import tweepy
import sys
import requests
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from bs4 import BeautifulSoup

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print('Authentication Successful')
except:
    print('Error while authenticating API')
    sys.exit(1)

response = requests.get('https://www.worldometers.info/coronavirus/country/malaysia/')
# print(response.content)
soup = BeautifulSoup(response.content, 'lxml')
numbers = soup.findAll("div", {"class": "maincounter-number"})
# print(numbers)
data = []
dataName = ['Total Cases', 'Deaths', 'Recovered']
for i in numbers:
    data.append(i.text)

newData = dict(zip(dataName, data))


tweet = f'''Coronavirus Latest Updates
Total cases: {newData['Total Cases']}
Recovered: {newData['Recovered']}
Deaths: {newData['Deaths']}
Source: https://www.worldometers.info/coronavirus/
#coronavirus #covid19 #coronavirusnews #coronavirusupdates
'''

api.update_status(tweet)
print('Tweet Successful')