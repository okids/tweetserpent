import pandas as pd
import logging
import re
import os
import pymysql
from datetime import date


def create_csv_header(BRAND_OBJECT):
    PANDAS_OUTFILE = os.getcwd()+'/data/'+BRAND_OBJECT+date.today().isoformat()+'.csv'
    PANDAS_SCHEMA = {
                    '_id': 0,
                    'user_id': 0,
                    'name': 0,
                    'created_at': 0,
                    'user_join': 0,
                    'tweet_id': 0,
                    'object': BRAND_OBJECT,
                    'geo':0,
                    'sentimen_result': 0,
                    'coordinates':0
                }
    pd_object = pd.DataFrame(PANDAS_SCHEMA, index=[0])
    try:
        with open(PANDAS_OUTFILE, 'a') as f:
            pd_object.to_csv(f, header=True)
        logging.info('Succes Creating File')
    except:
        logging.error('Failed Creating File')
        pass


def append_to_csv(BRAND_OBJECT, out):
    pd_object = pd.DataFrame(out, index=[0])
    PANDAS_OUTFILE = os.getcwd()+'/data/'+BRAND_OBJECT + date.today().isoformat()+ '.csv'
    if not os.path.exists(PANDAS_OUTFILE):
        create_csv_header(BRAND_OBJECT)
    try:
        with open(PANDAS_OUTFILE, 'a') as f:
            pd_object.to_csv(f, header=False)
            logging.info('Succes save tweet')
    except:
        logging.error('Failed save tweet : ' + out['text'])
        pass

def clean_tweet(tweet):
    return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|RT", " ",
           tweet)

def wordcount(tweet,word):
    if word in tweet.lower():
        return 1
    else:
        return 0

def create_sql_connection():
    return pymysql.connect(host='davidhutasoit.mysql.pythonanywhere-services.com',
                                 user='davidhutasoit',
                                 db='tweet_engine',
                                 charset='utf8mb4',
                                 password='datascience2016',
                                 cursorclass=pymysql.cursors.DictCursor)
