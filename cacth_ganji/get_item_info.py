from cacth_ganji import ganji_channel
from bs4 import BeautifulSoup
import requests
import re
import pymongo
import time
client = pymongo.MongoClient('127.0.0.1',port=27017)
cacth_ganji=client['cacth_ganji']
channel_urls = cacth_ganji['channel_urls']
item_urls = cacth_ganji['item_urls']
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'referer':'http://bj.ganji.com/wu/'}

def get_item_url(channel,page,who_sell=0):
    for i in channel:
        for p in page:
            channel_url='http://bj.ganji.com/{}/o{}'.format(i,p)
            if  channel_urls.find_one({'channel_url':channel_url}):
                continue
            wb_text=requests.get(channel_url)
            soup = BeautifulSoup(wb_text.text,'lxml')
            # if len(soup.select('li.js-item a.ft-tit')) == 5 and '抱歉' in soup.select('div.no-search dl dd ')[0].text:
            if not soup.select('li a.next span'):
                print('这个页面被抛弃，因为不存在',channel_url)
                break
            if not channel_urls.find_one({'channel_url':channel_url,'crawled':'false'}) and 'sorry' not in channel_url:
                print('哈哈,已经设定目标',channel_url)
                channel_urls.insert({'channel_url':channel_url,'crawled':'false'})
            time.sleep(2)

def url_spider():
    for i in channel_urls.find({'crawled':'false'}):
        wb_text=requests.get(i['channel_url'],headers=headers)
        soup=BeautifulSoup(wb_text.text,'lxml')
        urls=[b.get('href') for b in soup.select('ul li.js-item a.ft-tit') ]
        for a in urls:
            if 'click' in a and not item_urls.find_one({'item_url':a}):
                wb_te=requests.get(a)
                item_urls.insert({'item_url':wb_te.url})
                print('哈哈，已经设定目标',wb_te.url)
            elif not item_urls.find_one({'item_url':a}):
                item_urls.insert({'item_url':a})
                print('哈哈，已经设定目标',wb_te.url)
        channel_urls.update({'_id':i['_id']},{'$set':{'crawled':'true'}})
        time.sleep(2)

get_item_url(ganji_channel.get_all_channel(),range(1,1000))
url_spider()



