#test data
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import pickle


sample = pd.read_csv('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Sentiment Analysis/AllTweets.csv', sep=',',header=0)
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

features = pickle.load(open("C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Hashtags Topic Model/AsterixData/Exported Oct_16/features.p","rb"))


sns.set(font_scale=1.5)

logreg = LogisticRegression(C=1e9)
X = features
y = labels
logreg.fit(X, y)
predictions = logreg.predict(X)








