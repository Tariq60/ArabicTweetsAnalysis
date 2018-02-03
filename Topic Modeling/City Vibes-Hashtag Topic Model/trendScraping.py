import urllib
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy

'''
obj = urllib.urlopen("https://twitter.com/6areg")

t = open("twt_web.txt", "w")
[t.write(line) for line in obj.readlines()]
t.close()
'''

consumer_key = "GzU75msNH5HuVrzHBM1nocS8W"
consumer_secret = "edLOg5vySf2pYEANA5StrfT88HTNCTGoUBinS26ruJRxLkRjUv"
access_token = "245488245-Id8nbrLdIx1ejZbmN6Lmb4fNOxp7AW2g16v31Nwf"
access_token_secret = "RVtZh6Eu7Q3Nz4dsyLH0o1u3cWOoJJ0uDnpTziRpY39be"


#trend_url = "https://api.twitter.com/1.1/trends/place.json"


#twitter = Twitter( auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])


    api = tweepy.API(auth)
    #api.me()

    trendss = api.trends_place(1939753)          # list of 1 item, Sending ID of Riyadh, Saudi Arabia
    trends = trendss[0]                          # dict of 4 keys:   as_of, created_at, locations, trends
    t =trends['trends']                         # list of trends, size varies!

    
    for record in t:
        print record['name']                    # dict of 5 keys: name, promoted_content, query, tweet_volume, url






# In order to automate this Riyadh trends Collection that followed by collecting tweets from each trend, I need to do:
'''
1. Get Trends every six hours from Twitter API
2. Store Trends with Tweets, i.e. filter out the ones with "tweet_volume = None"
3. Trends should be exported in a csv file while making sure there are no redandunt trends.
4. Start the feed on AsterixDB to start Collecting tweets from trends in the csv file
===== Once a week
5. Export tweets in each trend in a seperate txt file to build the topic model
'''

