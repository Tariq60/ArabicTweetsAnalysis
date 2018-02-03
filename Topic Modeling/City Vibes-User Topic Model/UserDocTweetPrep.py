# -"- coding: utf-8 -"-
from __future__ import division
import pandas as pd
import re
import pickle
import string
import os

os.chdir("C:\\Users\\Tariq\\Dropbox (MIT)\\Projects\\3. ITS\\User Topic Model")

files_in_directory = 111
docs = [ [] for i in range(files_in_directory) ]
usertweets = []
for i in range(files_in_directory):
    print i
    user = pd.read_csv("User"+str(i)+".txt", sep=';', header=0, index_col = False)
    tweets = user['text'].values
    if len(tweets) > 1000 : tweets = tweets[0:1000]
    usertweets.append(len(tweets))
    for j in range(0, len(tweets)):
        if type(tweets[j]) == str:
            words = re.findall("[ء-غف-ي#_]+",tweets[j])
            for word in words:
                docs[i].append(word)
        else:
            continue

for i in range(0,len(docs)):
    for j in range(0,len(docs[i])):
        docs[i][j] = string.replace(docs[i][j],"أ","ا")
        docs[i][j] = string.replace(docs[i][j],"إ","ا")
        docs[i][j] = string.replace(docs[i][j],"اً","ا")
        docs[i][j] = string.replace(docs[i][j],"ؤ","و")
        docs[i][j] = string.replace(docs[i][j],"ئ","ي")


texts = [ [] for i in range(files_in_directory) ]

for j in range(0,len(docs)):
    for word in docs[j]:
        try: texts[j].append(word.decode('utf-8'))
        except: print "Exception!! >>" + word

pickle.dump( texts, open( "Userdocs.p", "wb" ) )

#words = string.replace(tweets[0],"\\n"," ")
#words = words.split()

texts = pickle.load(open("Userdocs.p","rb"))


