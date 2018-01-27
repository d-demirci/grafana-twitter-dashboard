import tweepy
import sys
import json
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch


consumer_key="TWITTER_CONSUMER_KEY"
consumer_secret="TWITTER_CONSUMER_SECRET"

access_token="TWITTER_ACCESS_TOKEN"
access_token_secret="TWITTER_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#es = Elasticsearch()
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'send_get_body_as':'POST' } ])

class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            #print 'n%s %s' % (status.author.screen_name, status.created_at)

            json_data = status._json
            #print json_data['text']

            es.index(index="idx_tweet",
                      doc_type="twitter_twp",
                      body=json_data
                     )

        except Exception as e:
            print (e)
            pass

streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000 )

#Fill with your own Keywords bellow
terms = ['visualize','elasticsearch','grafana']

streamer.filter(None,terms)
#streamer.userstream(None)
