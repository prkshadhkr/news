# import os
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, Article, Board, Feed, Source, User

from secrets import API_KEY
import requests

BASE_URL = "http://newsapi.org/v2/"

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgres:///news_db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///news_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SECRET_KEY'] = "very-secrets"

toolbar = DebugToolbarExtension(app)

connect_db(app)

#####################################################################

# url1 = (f"{BASE_URL}top-headlines?country=us&apiKey={API_KEY}")
# res1 = requests.get(url1)
# data1 = res1.json()
# articles1 = data1['articles']
# for article in articles1:
#     print('Headline US--->>>', article['title'])



# url2 = (f"{BASE_URL}top-headlines?country=us&category=entertainment&apiKey={API_KEY}")
# res2 = requests.get(url2)
# data2 = res2.json()
# articles2 = data2['articles']
# for article in articles2:
#     print('Entertainment Title--->>>', article['title'])


# url3 = (f"{BASE_URL}everything?q=apple&from=2020-04-25&to=2020-04-25&sortBy=popularity&apiKey={API_KEY}")
# res3 = requests.get(url3)
# data3 = res3.json()
# articles3 = data3['articles']
# for article in articles3:
#     print('Apple related Title--->>>', article['title'])


# url4 = (f"{BASE_URL}top-headlines?sources=cnn&apiKey={API_KEY}")
# res4 = requests.get(url4)
# data4 = res4.json()
# articles4 = data4['articles']
# print(articles4[0])
# for article in articles4:
#     print('CNN Title--->>>', article['title'])

def headline(country):
    url = (f"{BASE_URL}top-headlines?country={country}&apiKey={API_KEY}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles


#################

@app.route('/')
def index():
    news = headline('us')
    return render_template('news/index.html', news=news)
