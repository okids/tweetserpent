import pandas as pd
import re
import pickle
import os
import json
import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier


def print_topic(model, feature_names, n_top_word):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topic_dict = [{"keyword": feature_names[i], "score": topic[i]}
                      for i in topic.argsort()[:-n_top_word - 1:-1]]
        topic_dict.sort(key=lambda x: x.get("score"), reverse=True)
        topics.append(topic_dict)

    file_name = 'Topic.json'
    json_output_dir = os.path.join(os.getcwd(), file_name)
    with open(json_output_dir, 'w') as f:
        json.dump(topics, f)
    return topics


def print_top_words(data, n_top_words=20):
    for topic_idx, topic in enumerate(data):
        plt.figure()
        plt.imshow(WordCloud().fit_words(
            [(i["keyword"], i["score"])
             for i in topic[:-n_top_words - 1:-1]]
        ))
        plt.axis("off")
        plt.title("Topic #%d" % (topic_idx + 1))
        plt.savefig("Topic_" + str(topic_idx + 1) + ".png")
    print()

stops = stop_words = [line.strip() for line in open("indonesia.txt")]
train_anies = pd.read_csv(
    "DATA_ANIES_FIX.csv"
)

train_anies = train_anies.replace("1", "anies+")
train_anies = train_anies.replace("0", "anies-")

train_ahok = pd.read_csv(
    "data_training_ahok.csv"
)

train_ahok = train_ahok.replace("1", "ahok+")
train_ahok = train_ahok.replace("0", "ahok-")

train_ahy = pd.read_csv(
    "data_training_AHY.csv"
)

train_ahy = train_ahy.replace("1", "ahy+")
train_ahy = train_ahy.replace("0", "ahy-")

frames = [train_anies, train_ahok, train_ahy]

data_total = pd.concat(frames)

data_train = data_total[(data_total["Sentimen"] == "ahok+") | (data_total["Sentimen"] == "ahok-") | (data_total["Sentimen"] == "ahy+") | (data_total["Sentimen"] == "ahy-") | (data_total["Sentimen"] == "anies+") | (data_total["Sentimen"] == "anies-")]
data_train = data_train.reset_index(drop=True)

clean_train_tweet = []
sentiment_all = []

for i in range(len(data_train["_id"])):
    clean_train_tweet.append(' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|RT", " ",
               data_train["_id"][i]).split()))

for i in range(len(data_train["Sentimen"])):
    sentiment_all.append(data_train["Sentimen"][i])

vectorizer = TfidfVectorizer(analyzer="word",
                             stop_words=stops, min_df=0.001, max_df=0.85)

train_data_features = vectorizer.fit_transform(clean_train_tweet)
x_train, x_test, y_train, y_test = train_test_split(
    train_data_features, sentiment_all, test_size=0.3, random_state=42
)
train_data_features = x_train.toarray()

model = OneVsRestClassifier(LinearSVC(random_state=0))
model_fit = model.fit(train_data_features, y_train)
result = model.predict(x_test)
print(accuracy_score(result, y_test))

filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))

filename = 'vectorizer.sav'
pickle.dump(vectorizer, open(filename, 'wb'))

#load
#loaded_model = pickle.load(open(filename, 'rb'))

print("Fitting LDA models with tf ")
lda_array = nmf = NMF(n_components=10)
lda_array.fit(train_data_features)

tfidf_feature_names = vectorizer.get_feature_names()
topics = print_topic(lda_array, tfidf_feature_names, 200)
print_top_words(topics, 200)

train_unique = pd.read_csv(
    "data_unique_users.csv"
)
train_unique = train_unique.replace(np.nan, " ")
clean_train_tweet_unique = []

for i in range(len(train_unique["_id"])):
    clean_train_tweet_unique.append(' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|RT", " ",
               train_unique["text"][i]).split()))

test_data_features = vectorizer.transform(clean_train_tweet_unique)
test_data_features = test_data_features.toarray()

result_unique = model.predict(test_data_features)

res_unique = result_unique.tolist()
pro_ahok = res_unique.count("ahok+")
pro_anies = res_unique.count("anies+")
pro_ahy = res_unique.count("ahy+")

add_ahok = (res_unique.count("ahy-")*res_unique.count("ahok+")/(res_unique.count("ahok+") + res_unique.count("anies+"))) + (res_unique.count("anies-")*res_unique.count("ahok+")/(res_unique.count("ahok+") + res_unique.count("ahy+")))
add_anies = (res_unique.count("ahy-")*res_unique.count("anies+")/(res_unique.count("anies+") + res_unique.count("ahok+"))) + (res_unique.count("ahok-")*res_unique.count("anies+")/(res_unique.count("anies+") + res_unique.count("ahy+")))
add_ahy = (res_unique.count("anies-")*res_unique.count("ahy+")/(res_unique.count("ahy+") + res_unique.count("ahok+"))) + (res_unique.count("ahok-")*res_unique.count("ahy+")/(res_unique.count("ahy+") + res_unique.count("anies+")))

total = (pro_ahok + add_ahok) + (pro_anies + add_anies) + (pro_ahy + add_ahy)

pres_ahok = (pro_ahok + add_ahok)/total*100
pres_anies = (pro_anies + add_anies)/total*100
pres_ahy = (pro_ahy + add_ahy)/total*100

print("elektabilitas ahy-sylvi " + str(pres_ahy))
print("elektabilitas ahok-djarot " + str(pres_ahok))
print("elektabilitas anies-sandi " + str(pres_anies))
