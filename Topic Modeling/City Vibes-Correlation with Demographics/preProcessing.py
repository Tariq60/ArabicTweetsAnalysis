# -*- coding: utf-8 -*-
import re
import pandas as pd

f = open('C:\\Users\\Tariq\\Dropbox (MIT)\\Projects\\3. ITS\\Tweet Topics-Demographics Corr\\all.txt','rb') 
gTweets = f.readlines()

gText, lat, lon = [], [], []
for tweet in gTweets:
    gText.append(tweet.decode('utf-8').split('"text": "')[1].split('", "place":')[0])
    lat.append(str(tweet).split('"coordinates": [ ')[1].split(',')[0])
    lon.append(str(tweet).split('"coordinates": [ ')[1].split(',')[1].split(' ]')[0][1:])

time = []
for tweet in gTweets:
    time.append(str(tweet).split('"created_at": "')[1].split('"')[0])


day,month,day_type,time_of_day = [],[],[],[]
for t in time:
    row = t.split()
    day.append(row[0])
    month.append(row[1])
    day_type.append('wkend' if row[0] in ('Thu','Fri','Sat') else 'wkday')
    hour = int(row[3].split(':')[0])
    time_of_day.append('morning' if hour in range(6,12) else 'afternoon' if hour in range(12,18) else 'evening' if hour in range(18,24) else 'early_morning')
    
temporal_features = pd.DataFrame({'day':day, 'month':month, 'day_type':day_type, 'time_of_day':time_of_day})
# preprocess incoming Geotagged tweets before classifying
for i in range(0,len(gText)):
    gText[i] = gText[i].replace("ـ","")
    gText[i] = re.findall("[ء-غف-ي]+",gText[i])
    
# keeping words of length 3 and above!
#gText = [[token for token in text if len(token)>= 3] for text in gText]
# keeping tweets with more than 5 words
#gText = [text for text in gText if len(text) > 4]


f2 = open('tweets.txt','wb')
for text in gText:
    f2.write(text.encode('utf-8'))
    f2.write('\n')

