#Search Tweets in last 7 days by input()

#Import Modules
import tweepy #Twitter API
import timestring #Time conversion
from tweepy import OAuthHandler #Twitter Authentication
import twicreds #Password file
import json #json 
import time #for timer
import datetime as dt

print("Modules have been imported...")

#Authentication
def load_api():
        consumer_key = twicreds.consumer_key
        consumer_secret = twicreds.consumer_secret
        access_token = twicreds.access_token
        access_secret = twicreds.access_secret
        #auth = OAuthHandler(consumer_key, consumer_secret)
        #auth.set_access_token(access_token, access_secret)
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return tweepy.API(auth)

api = load_api()

print("Credentials have been assigned...")

#Test credentials
for tweet in tweepy.Cursor(api.search, q="PS4Share").items(10):
    try:
        print(type(tweet._json))
        print(tweet.text.encode('UTF-8').decode('UTF-8'))
    except ValueError:
        print("Unicode Error probably")
 
    except UnicodeEncodeError as f:
        print(f)
    except:
        print("Tweet experienced undefined error")
        

print("Setting up search criteria...")

#Search Criteria
print("to search for tweets containing either the word \"cupcake\" or \"donut\" you pass in the string \"cupcake OR donut\" as the q parameter.")
print("Please input your search query, using OR to insert multiple")
search_phrase = input()
time_limit = 1.0 # runtime limit in hours
min_days_old, max_days_old = 1, 8 #In days
max_tweets = 100
max_id = str()
since_id = str()
uk = api.geo_search(query="UK", granularity="country")
uk_id = uk[0].id #tweets in UK
usa = api.geo_search(query="USA", granularity="country")
usa_id = usa[0].id #tweets in USA
#France, Germany, 
europe_lat = api.geo_search(lat=54.5260, long=15.2551)
#54.5260° N, 15.2551° 

def tweet_search(api, query, max_tweets, max_id, since_id):
        searched_tweets = []
        while len(searched_tweets) < max_tweets:
                
                remaining_tweets = max_tweets - len(searched_tweets)
                #calculate remaining tweets before hitting limit
                try:
                        new_tweets = api.search(q=query, count=remaining_tweets, since_id=str(since_id), max_id=str(max_id))
                        if len(new_tweets) % 20 == 0:
                                print('found ' + str(len(new_tweets)) + ' tweets')
                        #print no. of tweets found
                        if not new_tweets: #if there's no new tweets
                                print('no tweets found')
                                break

                        searched_tweets.extend(new_tweets) #add new tweets to searched
                        max_id = new_tweets[-1].id #update id of last tweet
                except tweepy.TweepError:
                        print('exception raised, waiting 15 minutes')
                        print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
                        time.sleep(15*60) #sleep for 15 minutes
                        break # stop the loop
        return searched_tweets, max_id
print("Tweet search built, time to search....")

searched, max_id = tweet_search(api, search_phrase, max_tweets, max_id, since_id)

print("Testing entries from tweet search....")
print(searched[4])

print("declare filename to store tweets")
store_file = "\\Twitter\\" + input() + ".json"

import os
def write_tweets(tweets, filename):
        import os
        if os.path.exists(filename):
                append_write = 'a' # append if already exists
        else:
                append_write = 'w' # make a new file if not
        with open(filename, append_write) as f:
                for tweet in tweets:
                        json.dump(tweet._json, f)
                        f.write('\n')

write_tweets(searched, store_file)

print("file uploaded, would you like to upload again?")
answer = input()
if answer == "Yes" or "yes" or "Y":
        searched, max_id = tweet_search(api, search_phrase, max_tweets, max_id, since_id)
        print(type(searched[4]))
        write_tweets(searched, store_file)
                

"""
if processed_tweets:
        print(str(len(processed_tweets)) + " tweets were found")
        print(str(max_id) + " is the last tweet id accessed")

        print("Please give json file a filename...")
        filename = input()
        with open("\\Twitter\\" + filename + ".json", "w", encoding="utf-8") as f:
                        f.write(processed_tweets)

        print(str(filename) + " json file has been created")
        print("I'll see myself out now. Ciao")

else:
        print("No tweets found so no file will be created")
"""
#Set timer << Add to main search code
#max_time = int(input('Enter the amount of seconds you want to run this (e.g. 15 minutes = 60*15 = 900): '))
#start_time = time.time()  # remember when we started
#while (time.time() - start_time) < max_time:
