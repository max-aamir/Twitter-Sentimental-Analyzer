print("\n                 Twitter Sentiment Analyzer")
print("\n         Please wait, we are initializing modules......")

#     importing required modules

import time,sys,datetime
import json
import re
import matplotlib.pyplot as plt
import MyDB,resultGenerator

#     importing neccessary classes

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob

print("         Initialization complete. ")

#      initializing required variables

positive = 0
negative = 0
compound = 0
initime = time.time()
count = 0
nbm = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#     intialzing animated graph

plt.ion()

#     Authentication Keys and Consumer keys

ckey = 'CgRMME15L3zkE6U23gxTQf9Gl'
csecret = 'ORd3PDPj06aVBIUtafqG4OydHw7LlfWnn3pwPydubQhvHnTdb5'
atoken = '1027052893143093248-Wan94ss6ugHkca5JuzNoe2q71715Vh'
asecret = 'D4yCUtzHyvaxWK3Qq2iRcW52XdSfglOCKn9OYbixAaBjL'

#     Signing in to Twitter Account

print("     Loging in using your Twitter Account....")

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

print("     Login Successful.")

#     User Inputs

searchTerm = input(" Enter keyword/Tag to search about: ")
NoOfTerms = int(input(" Enter how many tweets you want to plot: "))

#     Calcultes the interval of time between tweets to plot accordingly

def calctime(a):
    return time.time()-a

#     Class to analyze data

class listener(StreamListener):

#     if data of a tweet found successfully on_data() otherwise on_error

    def on_data(self,data):

#     access global data variables rather than creating their own instance variables
        global initime , positive , negative , compound , count , NoOfTerms , nbm
        global searchTerm
        count = count +1
        senti = 0
        t = int(calctime(initime))

#     loads everything about the tweet time,location,user and many more
        all_data = json.loads(data)
        d = datetime.date.today()
        t1 = time.localtime()
        t1 = datetime.time(t1.tm_hour,t1.tm_min,t1.tm_sec)
        DTStamp = datetime.datetime.combine(d,t1)
        
        
        #print("Data ",data)
        print("---------------- Tweet ",count,"   ----------------")
        tweet = all_data["text"]
        #tweet = tweet.strip()
        tweet = tweet.translate(nbm)
        
        
        
        #print(type(tweet))
        print(" Tweet = ",tweet)
        tweet = " ".join(re.findall("[a-zA-z]+",tweet))
        blob = TextBlob(tweet.strip())
        #print(blob)
        for sen in blob.sentences:
            #print("sen  = ",sen)
            senti = senti + sen.sentiment.polarity
            if sen.sentiment.polarity>=0:
                positive = positive + sen.sentiment.polarity
            else :
                negative = negative + sen.sentiment.polarity
        compound = compound+senti
        
        val = (searchTerm,tweet,sen.sentiment.polarity,str(DTStamp))
        MyDB.insert(val)
        #print(" Sentiment = ",senti," Positive = ",positive," Negative = ",negative," Compound = ",compound)#print(" Time = ",t)
        plt.axis([0,100,-5,5])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t],[negative],'ro',[t],[compound],'bo') # ro - red go - green bo - blue
        plt.show()
        plt.pause(0.0001)
        if count>NoOfTerms-1 or count==200 :
            return False
        else:
            return True
    def on_error(self,status):
        print(status)

#     creating instance of Stream class and filtering tweets based on Search Term
twitterStream  = Stream(auth,listener(NoOfTerms))
twitterStream.filter(track=[searchTerm])
resultGenerator.result(searchTerm,"database.db")
