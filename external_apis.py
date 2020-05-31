from constants import  BASE_URL
from secrets import API_KEY

import requests

################## External API calls #######################

def news_headlines(country, page = 1):
    url = (f"{BASE_URL}/top-headlines?country={country}&apiKey={API_KEY}&page={page}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles

def news_headlines_sources(source):
    url = (f"{BASE_URL}/top-headlines?sources={source}&apiKey={API_KEY}&pageSize=100")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles

def news_categories(country, category, page = 1):
    url = (f"{BASE_URL}/top-headlines?country={country}&category={category}&apiKey={API_KEY}&page={page}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles


def news_sources():
    url = (f"{BASE_URL}/sources?apiKey={API_KEY}")
    res = requests.get(url)
    data = res.json()
    articles = data['sources']
    return articles

def news_search(search, page = 1):
    url = (f"{BASE_URL}/everything?q={search}&apiKey={API_KEY}&page={page}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles

def news_advsearch(search, fdate, tdate, page=1):
    url = (f"{BASE_URL}/everything?q={search}&from=\
        {fdate}&to={tdate}&sortBy=popularity&apiKey={API_KEY}&page={page}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles