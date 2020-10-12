"""SQLAlchemy models and utilities function for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB. String(15), nullable=False)

    def __repr__(self):
        return '-User {}-'.format(self.name)

class Tweet(DB.Model):
    """Tweet text and data. """
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    # Now we need a Foreign Key, pointing to the user who made the tweet.
    # In one-to-many relationship, the relation comes from the many side.
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)     
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)

def insert_example_users():
    """ example data to play with """
    austen = User(id=1, name='austen')
    elon = User(id=2, name='elonmusk')
    DB.session.add(austen)
    DB.session.add(elon)
    DB.session.commit()


