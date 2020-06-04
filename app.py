import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from forms import UserEditForm, LoginForm, AddForm, CountryForm, CategoryByCountry
from models import db, connect_db, Article, Board, Feed, Source, User, SourceFeed, ArticleBoard
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from external_apis import news_headlines, news_domains, news_categories, news_sources, news_search, news_advsearch
from config import per_page, total

from flask_paginate import Pagination, get_page_parameter
from tld import get_tld

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///news_db'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///news_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# app.config['SECRET_KEY'] = "very-secrets"

toolbar = DebugToolbarExtension(app)

connect_db(app)


######################### helper functions ##############################

def update_articles(data):

    source_id = data['source_id'] or 'NA'
    author = data['author']
    title = data['title'] 
    description = data['description'] 
    url = data['url']
    img_url = data['img_url'] 
    published_at = data['published_at'] 
    content = data['content'] 

    boards = data['board_id']

    article = Article(source_id=source_id,
                        author=author,
                        title=title,
                        description=description,
                        url=url,
                        img_url=img_url,
                        published_at=published_at,
                        content=content)
        
    db.session.add(article)
    db.session.commit()
        
    for board in boards:
        board_id = board
        article_id = article.id

        article_board = ArticleBoard(board_id=board_id, article_id=article_id)
        db.session.add(article_board)
        db.session.commit()

    return


################################## Routes ####################################

@app.route('/')
def index():
    return render_template('news/index.html')

@app.route('/headlines', methods=['GET', 'POST'])
def page_headlines():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    article_boards = db.session.query(ArticleBoard.board_id, Article.url).join(Article).all()

    form = CountryForm(request.args, csrf_enabled=False)
    boards = (Board.query
                    .filter(Board.user_id == g.user.id)
                    .all())

    if request.method == 'GET':
        country=request.args.get('country') or g.user.country
    
        page = request.args.get(get_page_parameter(), type=int, default=1)
        try:
            news = news_headlines(country, page)
        except:
            return render_template('404.html')
        pagination = Pagination(page=page, per_page=per_page, total = 40)

        return render_template('news/headlines.html', news=news, 
                                    form=form, boards=boards,
                                    article_boards=article_boards, country=country,
                                    page_name="page_headlines", pagination=pagination)

    if request.method == 'POST':
        data = request.json
        update_articles(data)

        return jsonify(message="added")


@app.route('/categories', methods=['GET', 'POST'])
def page_categories():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    article_boards = db.session.query(ArticleBoard.board_id, Article.url).join(Article).all()

    form = CategoryByCountry(request.args, csrf_enabled=False)
    boards = (Board.query
                    .filter(Board.user_id == g.user.id)
                    .all())


    if request.method == 'GET' and request.args.get("btn_submit") == "categories":
        country = request.args.get("country") or g.user.country
        category = request.args.get("category")

        page = request.args.get(get_page_parameter(), type=int, default=1)
        try:
            news = news_categories(country, category, page)
        except:
            return render_template('404.html')
        pagination = Pagination(page=page, per_page=per_page, total=total)

        return render_template('news/categories.html', form=form, news=news, 
                                boards=boards, article_boards=article_boards,
                                page_name="page_categories", country=country, btn_submit="categories",
                                category=category, pagination=pagination)

    if request.method == 'GET':
        return render_template('news/categories.html', form=form)

    if request.method == 'POST':
        data = request.json
        update_articles(data)

        return jsonify(message="added")


@app.route('/sources', methods=['GET', 'POST'])
def page_sources():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    source_feeds = db.session.query(SourceFeed.source_id, SourceFeed.feed_id).all()

    if request.method == 'GET':
        
        page = request.args.get(get_page_parameter(), type=int, default=1)
        sources = Source.query.paginate(page = page, per_page = per_page)

        feeds = (Feed
                .query
                .filter(Feed.user_id == g.user.id)
                .all())

        return render_template('news/sources.html', sources=sources,
                            feeds=feeds, source_feeds=source_feeds)

    elif request.method == "POST":
        
        data = request.json
        source_id = data['source_id']
        feeds = data['feed_id']
        for feed in feeds:
            feed_id = feed
            source_id = source_id

            source_feed = SourceFeed(source_id=source_id, feed_id=feed_id)
            db.session.add(source_feed)
            db.session.commit()
        return jsonify(message="added")


@app.route('/search', methods=['GET', 'POST'])
def page_search():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    article_boards = db.session.query(ArticleBoard.board_id, Article.url).join(Article).all()

    boards = (Board.query
                    .filter(Board.user_id == g.user.id)
                    .all())

    if request.method == 'GET' and (request.args.get("search_type") == "general"):
        search = request.args.get('q') or None

        page = request.args.get(get_page_parameter(), type=int, default=1)
        try:
            news = news_search(search, page)
        except:
            return render_template('404.html')
        pagination = Pagination(page=page, per_page=per_page, total=total)
     
        return render_template('news/search.html', news=news,
                        boards=boards, article_boards=article_boards, search_type="general",
                        q= search,  page_name="page_search", pagination=pagination)

    if (request.method == 'GET') and (request.args.get("search_type") == "date_base"):
        search = request.args.get("q") or None

        today = date.today()
        month_ago = today - timedelta(30)

        from_date = request.args.get("fromDate") or month_ago.isoformat()
        to_date = request.args.get("toDate") or today.isoformat()

        if (date.fromisoformat(to_date) - date.fromisoformat(from_date)).days > 30:
            from_date = month_ago.isoformat()

        page = request.args.get(get_page_parameter(), type=int, default=1)
        try:
            news = news_advsearch(search, from_date, to_date, page)
        except:
            return render_template('404.html')
        pagination = Pagination(page=page, per_page=per_page, total=total)

        return render_template('news/search.html', news=news,
                            boards=boards, article_boards=article_boards, search_type="date_base",
                            q=search, from_date=from_date, to_date=to_date,
                            page_name="page_search", pagination=pagination)

    if request.method == 'GET':
        return render_template('news/search.html')

    if request.method == 'POST':
        data = request.json
        update_articles(data)

        return jsonify(message="added")


######################### Feeds #####################################

@app.route('/feeds', methods=["GET", "POST"])
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
                .filter(Feed.user_id == g.user.id)
                .all())

    return render_template('feeds/new.html', form=form, feeds=feeds)


@app.route('/feeds/<int:id>', methods=['GET', 'POST'])
def feed_news(id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    article_boards = db.session.query(ArticleBoard.board_id, Article.url).join(Article).all()

    boards = (Board.query
                    .filter(Board.user_id == g.user.id)
                    .all())

    if request.method == 'GET':
        feed = Feed.query.get_or_404(id)
        feed_name = feed.name
        source_feeds = feed.source_feeds
        domains =""
        if len(source_feeds) > 0:
            for source_feed in source_feeds:
                res = get_tld(source_feed.sources.url, as_object=True)
                domains += res.fld+','
            domains = domains[:-1]
          
            page = request.args.get(get_page_parameter(), type=int, default=1)
            try:
                news = news_domains(domains, page)
            except:
                return render_template('404.html')
            pagination = Pagination(page=page, per_page=per_page, total=total)  

            return render_template('news/feeds.html', feed_id=id, news=news, boards=boards, 
                                    feed_name=feed_name, article_boards=article_boards,
                                     pagination=pagination)

        else:
            flash("Please Add source in Feed", "danger")
            return redirect('/sources')
    
    if request.method == 'POST':
        data = request.json
        update_articles(data)

        return jsonify(message="added")


@app.route('/feeds/<int:id>/delete', methods=["POST"])
def feed_ddelete(id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    feed = Feed.query.get_or_404(id)

    if feed.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    SourceFeed.query.filter(SourceFeed.feed_id == feed.id).delete()
    db.session.commit()

    db.session.delete(feed)
    db.session.commit()

    return redirect(f"/feeds")


@app.route('/feeds/<int:id>/<name>/delete', methods=["POST"])
def source_delete(id, name):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    source_id = SourceFeed.query.filter((SourceFeed.feed_id==id) & 
                                        (SourceFeed.source_id==name)).first()

    if source_id.feeds.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    SourceFeed.query.filter((SourceFeed.feed_id==id) & 
                            (SourceFeed.source_id==name)).delete()
    db.session.commit()
    
    return redirect(f"/feeds")


######################### boards #####################################

@app.route('/boards', methods=["GET", "POST"])
def board_add():
    """Add a board:
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AddForm()

    if form.validate_on_submit():
        name=form.name.data  

        board = Board(name=name)
        g.user.boards.append(board)
        db.session.commit()

        flash("Board created", "success")

    boards = (Board
                .query
                .filter(Board.user_id == g.user.id)
                .all())

    return render_template('boards/new.html', form=form, boards=boards)


@app.route('/boards/<int:id>', methods=['GET', 'PATCH', 'POST'])
def board_news(id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if request.method == 'GET':
        board = Board.query.get_or_404(id)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        article_boards = ArticleBoard.query.filter(ArticleBoard.board_id==id)\
                            .order_by(ArticleBoard.id.desc()).paginate(page = page, per_page = per_page)

        return render_template('news/boards.html', board=board, article_boards=article_boards)

    if request.method == 'PATCH':
        
        data = request.json
        article_id = data['id']

        article_board = ArticleBoard.query.filter((ArticleBoard.board_id==id) & 
                                            (ArticleBoard.article_id==article_id)).first()
                                        
        if article_board.is_read == False:
            article_board.is_read = True
        elif article_board.is_read == True:
            article_board.is_read = False

        db.session.commit()
        return jsonify(message="updated")
    
    if request.method == 'POST':
        
        data = request.json
        article_id = data['id']
        article = Article.query.get_or_404(article_id)
        
        ArticleBoard.query.filter((ArticleBoard.board_id==id) & 
                                    (ArticleBoard.article_id==article.id)).delete()
        
        db.session.commit()
        db.session.delete(article)
        db.session.commit()

        return jsonify(message="deleted")


@app.route('/boards/<int:id>/delete', methods=['POST'])
def board_delete(id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    board = Board.query.get_or_404(id)
    articles = board.articles

    if board.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    ArticleBoard.query.filter(ArticleBoard.board_id == board.id).delete()
    db.session.commit()

    if len(articles) > 0:
        for article in articles:
            db.session.delete(article)
            db.session.commit()

    db.session.delete(board)
    db.session.commit()

    return redirect(f"/boards")


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
            user.country= form.country.data or None
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
           
            return redirect("/headlines")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")


####################### contact ###################

@app.route('/contact')
def page_contact():
    return render_template("contact.html")


##################### Error #######################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')