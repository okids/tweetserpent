import pandas as pd
import re
import pickle
import os
import json
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score


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
train = pd.read_csv(
    "data_training_ahok.csv"
)

data_train = train[(train["Sentimen"] == "1") | (train["Sentimen"] == "0")]
data_train = data_train.reset_index(drop=True)

clean_train_tweet = []
sentiment_all = []

for i in range(len(data_train["_id"])):
    clean_train_tweet.append(' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|RT", " ",
               data_train["_id"][i]).split()))

for i in range(len(data_train["_id"])):
    sentiment_all.append(data_train["Sentimen"][i])

vectorizer = TfidfVectorizer(analyzer="word",
                             stop_words=stops)

train_data_features = vectorizer.fit_transform(clean_train_tweet)
x_train, x_test, y_train, y_test = train_test_split(
    train_data_features, sentiment_all, test_size=0.3, random_state=42
)
train_data_features = x_train.toarray()

model = LinearSVC()
model_fit = model.fit(train_data_features, y_train)
result = model.predict(x_test)
print(accuracy_score(result, y_test))

filename = 'model_ahok.sav'
pickle.dump(model, open(filename, 'wb'))

#load
#loaded_model = pickle.load(open(filename, 'rb'))

print("Fitting LDA models with tf ")
lda_array = nmf = NMF(n_components=10)
lda_array.fit(train_data_features)

tfidf_feature_names = vectorizer.get_feature_names()
topics = print_topic(lda_array, tfidf_feature_names, 200)
print_top_words(topics, 200)
