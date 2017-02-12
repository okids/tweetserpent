import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score


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
