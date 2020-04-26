# from newsapi import NewsApiClient

from secrets import API_KEY
import requests


BASE_URL = "http://newsapi.org/v2/"


url1 = (f"{BASE_URL}top-headlines?sources=techcrunch&apiKey={API_KEY}")
res1 = requests.get(url1)
data1 = res1.json()
articles1 = data1['articles']
for article in articles1:
    print('Headline of techChrunch Title--->>>', article['title'])



url2 = (f"{BASE_URL}top-headlines?country=in&category=entertainment&apiKey={API_KEY}")
res2 = requests.get(url2)
data2 = res2.json()
articles2 = data2['articles']
for article in articles2:
    print('Entertainment Title--->>>', article['title'])


url3 = (f"{BASE_URL}everything?q=apple&from=2020-04-25&to=2020-04-25&sortBy=popularity&apiKey={API_KEY}")
res3 = requests.get(url3)
data3 = res3.json()
articles3 = data3['articles']
for article in articles3:
    print('Apple related Title--->>>', article['title'])


url4 = (f"{BASE_URL}top-headlines?country=us&category=science&apiKey={API_KEY}")
res4 = requests.get(url4)
data4 = res4.json()
articles4 = data4['articles']
for article in articles4:
    print('Science Title--->>>', article['title'])
