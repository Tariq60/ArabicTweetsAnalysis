# -"- coding: utf-8 -"-


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Visualization_Summer_2016/arabic_tweets.dict')
corpus = corpora.MmCorpus('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Visualization_Summer_2016/arabic_tweets.mm')
print(corpus)


#tfidf = models.TfidfModel(corpus)     # step 1 -- initialize a model
#corpus_tfidf = tfidf[corpus]          # step 2 -- use the model to transform vectors 

lda = models.LdaModel(corpus, id2word=dictionary, num_topics=9)
lda.print_topics()

index = similarities.MatrixSimilarity(lda[corpus])

#test data
import pandas as pd
import re
sample = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Sentiment Analysis/AllTweets.csv', sep=',',header=0)
sample = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Visualization_Summer_2016/tweets_with_time3.csv', sep=',',header=0)
tweets = sample['content'].values

def fix_unicode(text):
    words = []
    for t in range(0,len(text)):
        text[t] = re.sub("<U\+([0-9A-F]{4})>", "\u\\1", text[t])
        #print t
        text[t] = text[t].decode('unicode_escape')
        words.append(text[t].split())
    return text

tweets = fix_unicode(tweets)


topics = []
for i in range(0,len(tweets)):
    vec_bow = dictionary.doc2bow(tweets[i].lower().split())
    #topics[i] = lda.get_document_topics(new_vec)
    vec_lda = lda[vec_bow]
    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    topics.append(sims[0][0])          #store the topic ID 

topics = []
for tweet in tweets:
	vec_bow = dictionary.doc2bow(tweet.lower().split())
	s = lda.get_document_topics(vec_bow)
	s = sorted(s, key=lambda item: -item[1])
	topics.append(s[0][0])
		
		
file = open("C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Sentiment Analysis/my work/newfile2.txt", "w")
for i in range(0,len(topics)):
	file.write(str(topics[i])+"\n")