from bokeh.charts import *
from bokeh.plotting import *
from sql_query import *
import os
import pandas as pd

def word_counter_generator():
    list_words = ['ahok','anies','djarot','sandi']
    word_counter=[]
    lists=[]
    for word in list_words:
        word_counter.append(fetch_word_counter(word))
        lists.append(word.title()+' : ' +  str(fetch_word_counter(word)))

    data = pd.Series(word_counter, index = lists)
    pie_chart = Donut(data)
    output_file(os.getcwd()+"/templates/word_count.html", title="Word Count")
    save(pie_chart)

def sentiment_generator():
    list_object = ['Ahok','Anies']
    object_counter=[]
    lists=[]
    for obj in list_object:
        for keys in fetch_sentimen_counter(obj):
            if keys != 'NEUTRAL_COUNTER':
                print(keys)
                object_counter.append(fetch_sentimen_counter(obj)[keys])
                lists.append(obj.title()+' ' + str(keys).title().split(sep='_')[0] +' : ' +  str(fetch_sentimen_counter(obj)[keys]))

    data = pd.Series(object_counter, index = lists)
    pie_chart = Donut(data)
    output_file(os.getcwd()+"/templates/sentiment_count.html", title="Sentiment Count")
    save(pie_chart)

word_counter_generator()
sentiment_generator()
