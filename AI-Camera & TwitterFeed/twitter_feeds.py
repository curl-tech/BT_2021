import os
import json
import urllib

from datetime import datetime

import tweepy as tw
from tweepy import Stream
from tweepy.streaming import StreamListener
import requests

# defining the api-endpoint 
URL = "http://localhost:8080/nature/upload-file"

class listener(StreamListener):

    def on_data(self, data):
        data_json = json.loads(data)
        
        if 'media' in data_json["entities"]:
            # Only 1st image will be downloaded
            for image in  data_json["entities"]['media']:
                dt = datetime.now()
                date_str = dt.strftime("%Y-%m-%d %H-%M-%S-%f")
                filename_str = "img_" + date_str + ".jpg"
                link = image['media_url']
                filename = os.path.join("images", filename_str)
                urllib.request.urlretrieve(link, filename)
                print("Image Downloaded")

                #Uploading files to frontend
                files = {'file': open(filename, 'rb')}
                data = {
                    "artName":f"TwitterArt",
                    "artDescription":"Coming From Twitter"
                }
                r = requests.post(URL, files=files, data=data)
                print("Image uploaded....!")   
                break
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    api_key = "TWITTER_API_KEY"
    api_secret = "TWITTER_API_SECRET"

    access_token = "ACCESS_TOKEN_GOES_HERE"
    access_token_secret = "ACCESS_TOKEN_SECRET_GOES_HERE"

    tags = ["#SattvaNFT"]

    auth = tw.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)

    sl = listener()
    twitterStream = Stream(auth=api.auth, listener=sl, tweet_mode='extended', include_entities=True)

    twitterStream.filter(track=tags)


