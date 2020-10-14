import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user1_name, user2_name, tweet_text):
    """
    Determine and return which user is more likely to say a given Tweet.
    
    Example: predict_user('ausen', 'elonmusk', 'Lambda School Rocks!')
    Returns 1 corresponding to 1st user passed in, or 0 for second.
    """
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_vect = np.array([tweet.vect for tweet in user1.tweets])
    user2_vect = np.array([tweet.vect for tweet in user2.tweets])

    vects = np.vstack([user1_vect, user2_vect])
    labels = np.concatenate([np.ones(len(user1.tweets)), 
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(vects, labels)
    # We've done the model fitting, now to predict...
    hypo_tweet_vect = vectorize_tweet(tweet_text)
    return log_reg.predict(np.array(hypo_tweet_vect).reshape(1,-1))
