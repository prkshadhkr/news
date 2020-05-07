# import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserEditForm, LoginForm, AddForm, COUNTRIES
from models import db, connect_db, Article, Board, Feed, Source, User

from secrets import API_KEY
import requests
from datetime import date



CURR_USER_KEY = "curr_user"
BASE_URL = "http://newsapi.org/v2"

CATEGORIES = ["", "business", "entertainment", "general", "health", "science", "sports", "technology"]

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgres:///news_db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///news_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SECRET_KEY'] = "very-secrets"

toolbar = DebugToolbarExtension(app)

connect_db(app)

###############################   API Requests ###############################

def news_headlines(country):
    url = (f"{BASE_URL}/top-headlines?country={country}&apiKey={API_KEY}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles

def news_categories(country, category):
    url = (f"{BASE_URL}/top-headlines?country={country}&category={category}&apiKey={API_KEY}")
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

def news_search(search):
   # url = (f"{BASE_URL}/top-headlines?q={search}&apiKey={API_KEY}")
    url = (f"{BASE_URL}/everything?q={search}&apiKey={API_KEY}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles

def news_advsearch(search, fdate, tdate):
    url = (f"{BASE_URL}/everything?q={search}&from={fdate}&to={tdate}&sortBy=popularity&apiKey={API_KEY}")
    res = requests.get(url)
    data = res.json()
    articles = data['articles']
    return articles



#########################  Routes ########################################

@app.route('/')
def index():
    return render_template('news/index.html')


@app.route('/headlines', methods=['GET', 'POST'])
def page_headlines():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user = g.user
 
    country = request.form.get('country') or g.user.country
    news = news_headlines(country)
    
    boards = (Board
                .query
                .filter(Board.user_id == g.user.id).distinct(Board.name)
                # .limit(20)
                .all())

    return render_template('news/headlines.html', news=news, countries=COUNTRIES, boards=boards)


@app.route('/categories', methods=['GET'])
def page_categories():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    country = request.args.get("country")or g.user.country
    category = request.args.get("category") 
    
    news = news_categories(country, category)

    return render_template('news/categories.html',countries=COUNTRIES, categories=CATEGORIES, news=news)


@app.route('/sources', methods=['GET'])
def page_sources():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    sources = Source.query.all()
    feeds = (Feed
                .query
                .filter(Feed.user_id == g.user.id).distinct(Feed.name)
                .all())
   
    return render_template('news/sources.html', sources=sources, feeds=feeds)


@app.route('/search', methods=['GET'])
def page_search():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    search = request.args.get('q')
    news = news_search(search)

    return render_template('news/everything.html', news=news, countries=COUNTRIES)


@app.route('/search/date', methods=['GET'])
def page_advsearch():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    search = request.args.get("q")
    from_date = request.args.get("fromDate") or None
    to_date = request.args.get("toDate") or date.today()

    news = news_advsearch(search, from_date, to_date)

    return render_template('news/advsearch.html', news=news)

######################### Feeds #####################################


@app.route('/feeds/new', methods=["GET", "POST"])
def feed_add():
    """Add a feed:
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AddForm()

    if form.validate_on_submit():
        name=form.name.data  

        feed = Feed(name=name)
        g.user.feeds.append(feed)
        db.session.commit()

        flash("Feed created", "success")

    feeds = (Feed
                .query
                .filter(Feed.user_id == g.user.id).distinct(Feed.name)
                .all())
    return render_template('feeds/new.html', form=form, feeds=feeds)


# @app.route('/feeds/<name>', methods=['GET', 'POST'])
# def page_feed(name):
    
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/login")

#     user = g.user
 
#     country = request.form.get('country') or g.user.country
#     news = news_headlines(country)
    
#     feeds = (Feed
#                 .query
#                 .filter(Feed.user_id == g.user.id).distinct(Feed.name)
#                 # .limit(20)
#                 .all())

#     return render_template('news/headlines.html', news=news, countries=COUNTRIES, boards=boards)


######################### Boards #####################################


@app.route('/boards/new', methods=["GET", "POST"])
def boards_add():
    """Add a board:
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AddForm()

    if form.validate_on_submit():
        name=form.name.data  

        # u_id = g.user.id

        # exists = Board.query.filter((Board.user_id==u_id) & (Board.name==name)) is not None
        
        # if exists:   
        #     flash("Board already exists", "danger")
        #     return redirect('/boards/new')

    
        board = Board(name=name)
        g.user.boards.append(board)
        db.session.commit()

        flash("Board created", "success")

    boards = (Board
                .query
                .filter(Board.user_id == g.user.id).distinct(Board.name)
                # .limit(20)
                .all())
    return render_template('boards/new.html', form=form, boards=boards)





########################## users #########################################

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('users/show.html', user=user)


@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.country= form.country.data
            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")



########################### User: signup/login/logout #################################

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
    form = UserEditForm()

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
