# -*- coding: utf-8 -*-
import sys,got,codecs
import pandas as pd

hashTweets = pd.read_csv('hashtags.csv',sep=';',header=0)        
text = hashTweets['text'].values
for i in range(0,len(text)):
    text[i] = unicode(text[i],"utf-8")

hashtags = []        
for tweet in text:
    for word in tweet.split():
        if word[0] == "#":
            hashtags.append(word)


#-------------------------------------------            Crawling Tweets in each Hashtags
reload(sys)
sys.setdefaultencoding('utf8')

for i in range(0,5):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hashtags[i].encode("utf8")).setMaxTweets(100)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    outputFile = codecs.open("Trend"+str(i)+".txt", "w+", "utf-8")
    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
    for t in tweets:
       outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
    outputFile.close()
    
'''
#checking the crawling working as expected

'''


