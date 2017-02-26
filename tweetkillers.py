#!/usr/bin/env python
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from util import create_csv_header, append_to_csv, clean_tweet, insert_to_sentimen_counter, insert_to_word_counter
from predictor import predictor
import logging
import json

logging.basicConfig(filename='log/tweepy.log',level=logging.DEBUG)
consumer_key = 'Qcgiz9RGTzoDGIE9xXp7I8g50'
consumer_secret = 'O9GAbvEB2sTpsWHQdqgckNHaH7kkYySZJFVUtQ0ivJZ3uJ3fPG'
access_token = '800349403894595584-CPaavTex9Mx15uw2KyZxlP6l3Y6HPOL'
access_secret = '6AwzMonNzowdo0Ri2NMNfqywIeCkSTJ02dg4oJAfbYzVu'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
BRAND_OBJECT = 'PILKADA'

create_csv_header(BRAND_OBJECT)
p = predictor()
p.load_model()

class StdOutListener(StreamListener):

    data = []
    errorStats = []

    def on_data(self, data):
        j = json.loads(data)
        try:
            u = j['user']
            p_res = p.predict(clean_tweet(j['text']))
            out = {
                '_id': (j['text']),
                'user_id': u['id'],
                'name': u['name'],
                'created_at': j['created_at'],
                'user_join': u['created_at'],
                'tweet_id': j['id'],
                'object': BRAND_OBJECT,
                'geo':j['geo'],
                'sentimen_result':p_res,
                'coordinates':j['coordinates']
            }
            append_to_csv(BRAND_OBJECT,out)
            insert_to_sentimen_counter(p_res)
            insert_to_word_counter(j['text'])


        except BaseException as e:
            print(e)
            return True

    def on_error(self, status):
        print(status)
        return True

l = StdOutListener()
stream = Stream(auth,l)
stream.filter(track=['ahok','anies','sandi','djarot'])

