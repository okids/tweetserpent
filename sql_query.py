from util import create_sql_connection

con = create_sql_connection()

def fetch_word_counter(word):
    cur = con.cursor()
    cur.execute("SELECT COUNTER FROM WORD_COUNTER WHERE WORD = %s", word)
    return cur.fetchall()

def fetch_sentimen_counter(object):
    cur = con.cursor()
    cur.execute("SELECT POSITIVE_COUNTER,NEGATIVE_COUNTER,NEUTRAL_COUNTER FROM SENTIMENT_COUNTER WHERE OBJECT = %s", object)
    return cur.fetchall()