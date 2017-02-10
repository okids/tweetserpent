#!/usr/bin/env python
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json

consumer_key = 'Qcgiz9RGTzoDGIE9xXp7I8g50'
consumer_secret = 'O9GAbvEB2sTpsWHQdqgckNHaH7kkYySZJFVUtQ0ivJZ3uJ3fPG'
access_token = '800349403894595584-CPaavTex9Mx15uw2KyZxlP6l3Y6HPOL'
access_secret = '6AwzMonNzowdo0Ri2NMNfqywIeCkSTJ02dg4oJAfbYzVu'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

c = MongoClient('localhost')
db = c['ts']
BRAND_OBJECT = 'AHOK'
class StdOutListener(StreamListener):

    data = []
    errorStats = []

    def on_data(self, data):
        j = json.loads(data)
        try:
            u = j['user']
            db.tweet.insert(
                {'_id': (j['text']), 'user_id': u['id'], 'name': u['name'], 'created_at': j['created_at'],
                             'user_join': u['created_at'], 'tweet_id':j['id'],'object':BRAND_OBJECT}
            )
            return True
        except BaseException as e:
            print(e)
            return True


    def on_error(self, status):
        print(status)
        return True

l = StdOutListener()
stream = Stream(auth,l)
stream.filter(track=['ahok','ahok djarot', 'djarot'])

