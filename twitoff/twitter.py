""" Retrieve Tweets, embeddings, and persist in the database. """

import tweepy 
import spacy
from .models import DB, Tweet, User
from os import getenv


TWITTER_USERS = ['calebhicks','elonmusk','rrherr','SteveMartinToGO',
                'alyankovic','nasa','sadserver','jkhowland','austen',
                'common_squirrel','KenJennngs','conanobrien',
                'big_ben_clock','IAM_SHAKESPEARE']

TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)  # connection object


nlp = spacy.load('my_model')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    """Add or update a user and their tweets, error if not a Twitter user. """

    try:  # try to get the info from Twitter, then try to put it into the database
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)
        # Now get the tweets, focusing on primary, not retweets and replies
        tweets = twitter_user.timeline(
                count=200, exclude_replies=True, include_rts=False, 
                tweet_mode = 'extended', since_id=db_user.newest_tweet_id
        )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print('Error Processiong {}: {}'.format(username, e))
        raise e 

    else:   # gets executed only if the entire "try" went ok and there was no "except"
        DB.session.commit()


def insert_example_users():
    """Example data to play with """
    add_or_update_user('elonmusk')
    add_or_update_user('jackblack')