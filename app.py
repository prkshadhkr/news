# import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import SignupForm, LoginForm, COUNTRIES
from models import db, connect_db, Article, Board, Feed, Source, User

from secrets import API_KEY
import requests

CURR_USER_KEY = "curr_user"
BASE_URL = "http://newsapi.org/v2"

CATEGORIES = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

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

# url1 = (f"{BASE_URL}/top-headlines?country=us&apiKey={API_KEY}")
# res1 = requests.get(url1)
# data1 = res1.json()
# articles1 = data1['articles']
# for article in articles1:
#     print('Headline US--->>>', article['title'])



# url2 = (f"{BASE_URL}/top-headlines?country=us&category=entertainment&apiKey={API_KEY}")
# res2 = requests.get(url2)
# data2 = res2.json()
# articles2 = data2['articles']
# for article in articles2:
#     print('Entertainment Title--->>>', article['title'])


# url3 = (f"{BASE_URL}/everything?q=apple&from=2020-04-25&to=2020-04-25&sortBy=popularity&apiKey={API_KEY}")
# res3 = requests.get(url3)
# data3 = res3.json()
# articles3 = data3['articles']
# for article in articles3:
#     print('Apple related Title--->>>', article['title'])


# url4 = (f"{BASE_URL}/top-headlines?sources=cnn&apiKey={API_KEY}")
# res4 = requests.get(url4)
# data4 = res4.json()
# articles4 = data4['articles']
# print(articles4[0])
# for article in articles4:
#     print('CNN Title--->>>', article['title'])

def news_headlines(country):
    url = (f"{BASE_URL}/top-headlines?country={country}&apiKey={API_KEY}")
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

#################

@app.route('/')
def index():

    news = news_headlines('us')
    return render_template('news/index.html', news=news)



@app.route('/headlines', methods=['GET', 'POST'])
def page_headlines():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")


    country = request.form.get('country') or g.user.country
    news = news_headlines(country)

    return render_template('news/headlines.html', news=news, countries=COUNTRIES)


@app.route('/categories', methods=['GET'])
def page_categories():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    categories = CATEGORIES

    return render_template('news/categories.html',categories=categories)



##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                country=form.country.data or User.country.default.arg
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/headlines")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            # return redirect("/")
            return redirect("/headlines")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")
