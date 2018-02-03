# -*- coding: utf-8 -*-
import sys,got,codecs
import pandas as pd
import os

os.chdir('C:\\Users\\Tariq\\Dropbox (MIT)\\Projects\\3. ITS\\User Topic Model')
top_users = pd.read_csv('infleuntial_users_Saudi.csv',sep=',',header=0)        
users = top_users['username'].values
types = top_users['Type'].values

tweets_per_user = []
for i in range(30,len(users)):
    tweetCriteria = got.manager.TweetCriteria().setUsername(users[i]).setMaxTweets(500)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    outputFile = codecs.open("User"+str(i)+".txt", "w+", "utf-8")
    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
    for t in tweets:
       outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s;%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink, types[i])))
    outputFile.close()
    tweets_per_user.append(len(tweets))
'''
#checking the crawling working as expected

'''


