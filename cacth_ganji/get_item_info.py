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
        'referer':'http://bj.ganji.com/wu/',
         'Connection': 'keep-alive'}

def get_item_url(channel,page,who_sell=0):
    for i in channel:
        for p in page:
            channel_url='http://bj.ganji.com/{}/o{}'.format(i,p)
            if  channel_urls.find_one({'channel_url':channel_url}):
                continue
            wb_text=requests.get(channel_url)
            soup = BeautifulSoup(wb_text.text,'lxml')
            if soup.select('.next') and len(soup.select('ul li.js-item a.ft-tit')) != 5:
                channel_urls.insert({'channel_url': channel_url, 'crawled': 'false'})
                print('哈哈,已经将该页插入到channel_urls库中了，可以被url_spider搞了',channel_url)
            else:
                print('由于下一页按钮没有或者该页面只select到5个条目,所以认为该页不存在', channel_url)
                break
            time.sleep(2)

def get_others_commodity_url_to_db(channel_url):
    #这三个类目下的商品页面属性不一样，杂七杂八 免费赠送 物品交换
    wb_text = requests.get(channel_url,headers=headers)
    soup = BeautifulSoup(wb_text.text,'lxml')
    urls=[b.get('href') for b in soup.select('a.infor-title01.com-title')]
    for a in urls:
        if 'click' in a and not item_urls.find_one({'item_url':a}):
            wb_text=requests.get(a,headers=headers)
            item_urls.insert({'item_url':wb_text.url})
            print('哈哈，已经将商品的详情页的url加入到item_urls库了')
        elif not item_urls.find_one({'item_url':a}):
            item_urls.insert({'item_url':a})
            print('哈哈，已经将商品的详情页的url加入到item_urls库了')
        channel_urls.update({'_id':i['_id']},{'$set':{'crawled':'true'}})
        time.sleep(2)
def url_spider():
    for i in channel_urls.find({'crawled':'false'}):
        print(i)
        if 'qitawupin' in i or 'ershoufree' in i or 'wupinjiaohuan' in i :
            get_others_commodity_url_to_db(i)
        else:
            wb_text=requests.get(i['channel_url'],headers=headers)
            soup=BeautifulSoup(wb_text.text,'lxml')
            urls=[b.get('href') for b in soup.select('ul li.js-item a.ft-tit') ]
            for a in urls:
                wb_te=requests.get(a)
                if 'click' in a and not item_urls.find_one({'item_url':a}):
                    item_urls.insert({'item_url':wb_te.url})
                    print('哈哈，已经设定目标',wb_te.url)
                elif not item_urls.find_one({'item_url':a}):
                    item_urls.insert({'item_url':a})
                    print('哈哈，已经设定目标',wb_te.url)
                channel_urls.update({'_id':i['_id']},{'$set':{'crawled':'true'}})
                time.sleep(2)

get_item_url(ganji_channel.get_all_channel(),range(1,1000))
url_spider()
# get_others_commodity_url_to_db('http://bj.ganji.com/wupinjiaohuan/o2')



