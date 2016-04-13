from cacth_ganji import ganji_channel
from bs4 import BeautifulSoup
import requests
import re
import pymongo
client = pymongo.MongoClient('127.0.0.1',port=27017)
cacth_ganji=client['cacth_ganji']
channel_urls = cacth_ganji['channel_urls']
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'referer':'http://bj.ganji.com/wu/'}
def get_item_url(channel,page,who_sell=0):
    for i in channel:
        for p in page:
            channel_url='http://bj.ganji.com/{}/o{}'.format(i,p)
            if not channel_urls.find_one({'channel_url':channel_url,'crawled':'false'}):
                channel_urls.insert({'channel_url':channel_url,'crawled':'false'})

def url_spider():
    # print(len(list(channel_urls.find({'crawled':'false'}))))
    for i in channel_urls.find({'crawled':'false'}):
        wb_text=requests.get(i['channel_url'],headers=headers)
        soup=BeautifulSoup(wb_text.text,'lxml')
        # urls=soup.select('ul li.js-item a.ft-tit')
        urls=[b.get('href') for b in soup.select('ul li.js-item a.ft-tit')]
        print(urls)
get_item_url(ganji_channel.get_all_channel(),range(4))
url_spider()
# print(list(channel_urls.find({'crawled':'false'})))



