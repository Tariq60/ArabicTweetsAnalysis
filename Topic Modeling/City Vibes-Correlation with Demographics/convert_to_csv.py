# Author: Tariq Alhindi       2/21/2017
# This code reads geo-tagged tweets in .txt format and export .csv file to be used later by QGIS to generates a shapefile for tweets in neighborhoods

import pandas as pd

f = open('C:\\Users\\Tariq\\Dropbox (MIT)\\Projects\\3. ITS\\zeyad-geo_tagged.txt','rb') 
gTweets = f.readlines()

gText = []
lat = []
lon = []
for tweet in gTweets:
    gText.append(tweet.decode('utf-8').split('"text": "')[1].split('", "place":')[0])
    lat.append(str(tweet).split('"coordinates": [ ')[1].split(',')[0])
    lon.append(str(tweet).split('"coordinates": [ ')[1].split(',')[1].split(' ]')[0][1:])
    

tweet2 = pd.DataFrame()
tweet2['txt']=gText
tweet2['lat']=lat
tweet2['lon']=lon
tweet2.to_csv("tweet2.csv")