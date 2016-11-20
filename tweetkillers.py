import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'Qcgiz9RGTzoDGIE9xXp7I8g50'
consumer_secret = 'O9GAbvEB2sTpsWHQdqgckNHaH7kkYySZJFVUtQ0ivJZ3uJ3fPG'
access_token = '800349403894595584-CPaavTex9Mx15uw2KyZxlP6l3Y6HPOL'
access_secret = '6AwzMonNzowdo0Ri2NMNfqywIeCkSTJ02dg4oJAfbYzVu'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class StdOutListener(StreamListener):

    data = []
    errorStats = []

    def on_data(self, data):
        try:
            print(data)
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("error on data")
            return True


    def on_error(self, status):
        print(status)
        return True

l = StdOutListener()
stream = Stream(auth,l)
stream.filter(track=['#tangkapAhok'])

