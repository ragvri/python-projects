import tweepy
import urllib
import json
import pprint

consumer_key = "tbnTCzkud5qpA5VxsyDafYSF6"
consumer_secret = "2tS7aSDTNEENHdFnrQDdYcJv7LZ5mcMiN2LmiowA6BeR2sjdzU"
access_token = "806380174807887873-JsD7fJSRbOjh9PxXPObcbphtl13oUv8"
access_token_secret = "rUNNFsKmrJvYorMrN0RKplTN79rltL1BoIGD4NgUl5YAZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)  # API class provides access to entire twitter Restful API methods

# this will download my home timeline tweets and print their texts on screen
public_tweets = api.home_timeline()
# for tweet in public_tweets:
# print(tweet.text)
user = api.get_user('ragvri')
print(user.followers_count)
print(user.screen_name)

# Iterate through all of the friends of user
for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    if follower.friends_count < 300:
        print(follower.screen_name)

for status in tweepy.Cursor(api.user_timeline, id="ragvri").items(10):  # can pass parameters to the cursor. Gets
    # the top 10 tweets by twitter
    print(status.text)

# post random chuck norris jokes
req = urllib.request.Request("http://api.icndb.com/jokes/random")
text = urllib.request.urlopen(req).read().decode('utf-8')
json_dict = json.loads(text)
joke = json_dict['value']['joke']
print(joke)

api.update_status(joke)
print('done')
