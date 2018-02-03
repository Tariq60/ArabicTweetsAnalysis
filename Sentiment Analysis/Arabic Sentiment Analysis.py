# -"- coding: utf-8 -"-
from __future__ import division
import nltk
import pandas as pd
import re


sample = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Sentiment Analysis/sampleTweets.csv', sep=',',header=0)
text = sample['text'].values
sentiment = sample['sentiment'].values


#------------ Functions --------------
def fix_unicode(text):
    words = []
    for t in range(1,len(text)):
        text[t] = re.sub("<U\+([0-9A-F]{4})>", "\u\\1", text[t])
        text[t] = text[t].decode('unicode_escape')
        words.append(text[t].split())
    return words

#--------------------------------------
words = fix_unicode(text)
#--------------------------------------

def text_sentiment(words,sentiment):
    tweets = []
    for t in range(1,len(words)):
        #words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
	tweets.append((words[t], sentiment[t]))
    return tweets

#--------------------------------------
tweets = text_sentiment(words,sentiment)
#--------------------------------------

def get_words_in_tweets(tweets):
	all_words = []
	for words in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
        wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features


#--------------------------------------
word_features= get_word_features(get_words_in_tweets(tweets))
#--------------------------------------	

def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features


#--------------------------------------
pos = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Sentiment Analysis/posTweet.csv', sep=',',header=0)
pos_tweets = pos['content'].values
pos_words = fix_unicode(pos_tweets)
pos_sentiment = pos['sentiment'].values
postweets = text_sentiment(pos_words,pos_sentiment)

neg = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Sentiment Analysis/negTweet.csv', sep=',',header=0)
neg_tweets = neg['content'].values
neg_words = fix_unicode(neg_tweets)
neg_sentiment = neg['sentiment'].values
negtweets = text_sentiment(neg_words,neg_sentiment)

alltweets = postweets + negtweets
word_features= get_word_features(get_words_in_tweets(alltweets))
training_set = nltk.classify.apply_features(extract_features, alltweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
print classifier.show_most_informative_features(32)
#-------------------------------------------

All = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Sentiment Analysis/AllTweets.csv', sep=',',header=0)
All_tweets = All['content'].values
All_words = fix_unicode(All_tweets)
All_sentiment = All['tweet_id'].values
Alltweets = text_sentiment(All_words,All_sentiment)
word_features= get_word_features(get_words_in_tweets(Alltweets))

