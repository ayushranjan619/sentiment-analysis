# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 15:07:13 2017

@author: admin
"""


import time
import smtplib
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

tweets=[]
user=[]
polar=[]



def email1(x):
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login("sender email address", "password")  

    # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
    SUBJECT="Need Support"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, x)

    server_ssl.sendmail("sender email address", "reciever email address",message)
    #server_ssl.quit()
    server_ssl.close()
    print('successfully sent the mail')






"# -- coding: utf-8 --"

def calctime(a):
    return time.time()-a

positive=0
negative=0
compound=0

count=0
initime=time.time()
plt.ion()

ckey=" "
csecret=" "
atoken="  "
asecret=" "

class listener(StreamListener):
    
    def on_data(self,data):
        try:
            global initime
            t=int(calctime(initime))
            all_data=json.loads(data)
            tweet=all_data["text"].encode("utf-8")
            username = all_data["user"]["screen_name"]
            user.append(username)
        #username=all_data["user"]["screen_name"]
            tweet=" ".join(re.findall("[a-zA-Z]+", tweet.decode()))
            blob=TextBlob(tweet.strip())

            global positive
            global negative     
            global compound  
            global count
        
            count=count+1
            senti=0
            for sen in blob.sentences:
                senti=senti+sen.sentiment.polarity
                tweets.append(tweet.strip())
                polar.append(sen.sentiment.polarity)
                if sen.sentiment.polarity >= 0:
                   positive=positive+sen.sentiment.polarity   
                else:
                    variable = "TWEET " + str(tweet.strip()) +'      '+ "USER " + str(username) +'      '+"negative sentiment"
                    email1(variable)
                    negative=negative+sen.sentiment.polarity  
            compound=compound+senti 
         
            print(count)
            print(tweet.strip())
            print(senti)
            #print(t)
            print(str(positive) + ' ' + str(negative) + ' ' + str(compound)) 
        
    
           # plt.axis([ 0, 100, -20,20])
            #plt.xlabel('Time')
            #plt.ylabel('Sentiment')
            #plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[compound],'bo')
            #plt.show()
            #plt.pause(0.0001)
            if count==5:
                return False
            else:
                return True
        except:
            return True
            
        
    def on_error(self,status):
        print(status)


auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["icici"])               #what you want to track


di={'polar':polar,'tweets':tweets}
import pandas as pd
tt=pd.DataFrame(di)

def func_sent(x):
    if x>0:
        return('positive')
    elif x<0:
        return('negative')
    else:
        return('neutral')
    
tt['sentiment']=tt['polar'].apply(func_sent)
tt.to_csv('twitter_sentiment.csv',index=False)

