import tweepy


consumer_key = '8y3JayTZMuulHAjN2G0qFaVA0'
consumer_secret = 'D6MvjTIVPYFqgf6jHzKfpQJoxleIsusDvGCirKHFzx8B6Zkk52'
access_token = '859623696780201984-TAPoYVCv1fevDLD8H6rmM5REdcrbfYr'
access_secret = 'sTnTGvtR0NDnCfADh7eDp3Yrh4dkqLgtSOCRqMHz157q7'


def get_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    return api