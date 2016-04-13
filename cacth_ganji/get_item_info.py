from cacth_ganji import ganji_channel
from bs4 import BeautifulSoup
import requests
import re
import pymongo
client = pymongo.MongoClient('127.0.0.1',port=27017)
cacth_ganji=client['cacth_ganji']
channel_urls = cacth_ganji['channel_urls']

def get_item_url(channel,page,who_sell=0):
    for i in channel:
        for p in page:
            channel_url='http://bj.ganji.com/{}/o{}'.format(i,p)
            channel_urls.insert({'channel_url':channel_url,'crawled':'false'})

get_item_url(ganji_channel.get_all_channel(),range(4))
