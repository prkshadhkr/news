"""Seed file to make sample data for db."""

from models import Article, Board, Feed, Source, User, db
from app import app, news_sources

# Create all tables
db.drop_all()
db.create_all()


######################### update database ###############################

sources = news_sources()
for source in sources:
    id = source['id']
    name = source['name']
    description = source['description']
    url = source['url']
    category = source['category']
    language = source['language']
    country = source['country']

    s = Source(id=id, name=name, description=description, url=url, category=category, language=language, country=country)
    db.session.add(s)
    db.session.commit()

    

###################  Make a bunch of tables for testing database schemas ######################


# s1 = Source(id="news1", name="NEWS1", description="news1 news", 
#             url="www.news1.com", category="general", language="en", country="us")
# s2 = Source(id="news2", name="NEWS2", description="news2 news", 
#             url="www.news2.com", category="general", language="en", country="us")
# s3 = Source(id="news3", name="NEWS3", description="news3 news", 
#             url="www.news3.com", category="general", language="en", country="gb")
# s4 = Source(id="news4", name="NEWS4", description="news4 news", 
#             url="www.news4.com", category="sports", language="en", country="us")
# s5 = Source(id="news5", name="NEWS5", description="news5 news", 
#             url="www.news5.com", category="general", language="en", country="us")

# db.session.add_all([s1, s2, s3, s4, s5])
# db.session.commit()

# # Make a bunch of articles
# a1 = Article(source_id="news5", author="Ben", title="I like cat", description="I am hungry", 
#             url="www.news5.com", img_url="www.news5.com/img.", published_at="2020-05-01", content="somthing..")
# a2 = Article(source_id="news1", author="Joe", title="friendly animals", description="dog are good friends", 
#             url="www.news1.com", img_url="www.news1.com/img.", published_at="2020-05-01", content="anything..")
# a3 = Article(source_id="news4", author="John", title="baseball season", description="no more sports", 
#             url="www.news4.com", img_url="www.news4.com/img.", published_at="2020-05-01", content="whatever you want..")
# a4 = Article(source_id="news3", author="Lisa", title="random article", description="not sure what is in", 
#             url="www.news3.com", img_url="www.news3.com/img.", published_at="2020-05-01", content="random content..")
# a5 = Article(source_id="news2", author="Monica", title="a day in Ny", description="around timesquare", 
#             url="www.news2.com", img_url="www.news2.com/img.", published_at="2020-05-01", content="empire state..")

# db.session.add_all([a1, a2, a3, a4, a5])
# db.session.commit()

# # # Make a bunch of users

# u1 = User.signup(username="firstuser", email="one@email.com", password="firstuser", country='us')
# u2 = User.signup(username="seconduser", email="two@email.com", password="seconduser", country='br')
# u3 = User.signup(username="thirduser", email="three@email.com", password="thirduser", country='ca')
# u4 = User.signup(username="fourthuser", email="four@email.com", password="fourthuser", country='us')
# u5 = User.signup(username="fifthuser", email="five@email.com", password="fifthuser", country='ae')


# db.session.add_all([u1, u2, u3, u4, u5])
# db.session.commit()



# # Add sample feeds
# f1 = Feed(user_id=1, name="my likes")
# f2 = Feed(user_id=1, name="sports only")
# f3 = Feed(user_id=2, name="likes")
# f4 = Feed(user_id=2, name="keep eyes on")
# f5 = Feed(user_id=3, name="first feed")

# db.session.add_all([f1, f2, f3, f4, f5])
# db.session.commit()


# # Add sample boards
# b1 = Board(user_id=1, name="must read")
# b2 = Board(user_id=1, name="read later")
# b3 = Board(user_id=3, name="second read")
# b4 = Board(user_id=3, name="reading list")
# b5 = Board(user_id=2, name="my board")

# db.session.add_all([b1, b2, b3, b4, b5])
# db.session.commit()