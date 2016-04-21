import ganji_channel
from bs4 import BeautifulSoup
import requests
import pymongo
import time
from multiprocessing import Pool
client = pymongo.MongoClient('127.0.0.1',port=27017)
cacth_ganji=client['cacth_ganji']
channel_urls = cacth_ganji['channel_urls']
item_urls = cacth_ganji['item_urls']
item_detail_info_db=cacth_ganji['item_detail_info_db']
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'referer':'http://bj.ganji.com/wu/',
         'Connection': 'keep-alive'}

def get_channel_url_to_db(channel,page,who_sell=0):
    #这个函数从http://bj.ganji.com/wu这个页面获取赶集网20个二手商品分类从这些页面生成每一页的数据比如
    #http://bj.ganji.com/jiaju/o2/这个网址，将这些url传给url_spider()函数去处理
    for i in channel:
        for p in page:
            channel_url='http://bj.ganji.com/{}/o{}'.format(i,p)
            if  channel_urls.find_one({'channel_url':channel_url}):
                print('这个在channel_url数据库中有了，直接下一条',channel_url)
                continue
            try:
                wb_text=requests.get(channel_url)
            except:
                print('这个页面在request的时候出了问题，抛弃',channel_url)
                channel_urls.insert({'channel_url':channel_url,'crawled':'networkproblem'})
            wb_text.encoding='utf-8'
            soup = BeautifulSoup(wb_text.text,'lxml')
            if soup.select('.next') and len(soup.select('ul li.js-item a.ft-tit')) != 5:
                channel_urls.insert({'channel_url': channel_url, 'crawled': 'false'})
                print('哈哈,已经将该页插入到channel_urls库中了，可以被url_spider搞了',channel_url)
            else:
                channel_urls.insert({'channel_url':channel_url,'crawled':'pageproblem'})
                print('由于下一页按钮没有或者该页面只select到5个条目,所以认为该页不存在', channel_url)
                break
            time.sleep(2)

def get_others_commodity_url_to_db(channel_url):
    #这三个类目下的商品页面属性不一样，杂七杂八 免费赠送 物品交换,所以如果遇到这三个类目会自动用这个函数处理
    try:
        wb_text = requests.get(channel_url,headers=headers)
    except:
        print('这个页面使用request方法请求出错了，丢弃',channel_url)
        channel_urls.update({'channel_url':channel_url},{'$set':{'crawled':'networkproblem'}})
        return False
    wb_text.encoding='utf-8'
    soup = BeautifulSoup(wb_text.text,'lxml')
    if soup.select('a.infor-title01.com-title') :
        urls=[b.get('href') for b in soup.select('a.infor-title01.com-title')]
    else:
        print('这个页面在做select的时候返回空抛弃',channel_url)
        channel_urls.update({'channel_url':channel_url},{'$set':{'crawled':'pageproblem'}})
        return False
    time.sleep(2)
    for a in urls:
        try:
            wb_text=requests.get(a,headers=headers)
        except:
            print('这个页面使用request方法请求出错了，丢弃',a)
            item_urls.insert({'item_url':a,'crawled':'networkproblem'})
            continue
        wb_text.encoding='utf-8'
        if 'sorry' in a:
            print('这条网址里含有sorry丢弃')
            continue
        elif 'click' in a and not item_urls.find_one({'item_url':a}):
            item_urls.insert({'item_url':wb_text.url})
            print('哈哈，已经将商品的详情页的url加入到item_urls库了')
        elif not item_urls.find_one({'item_url':a}):
            item_urls.insert({'item_url':a})
            print('哈哈，已经将商品的详情页的url加入到item_urls库了',a)



def url_spider(channel_url):
    #这个函数负责将get_item_url()生成的页面的父级url进行处理，每一个url可以获得60条具体的商品详情页面的url
    try:
        wb_text=requests.get(channel_url,headers=headers)
    except:
        print('这个页面使用request方法请求出错了，丢弃',channel_url)
        return False
    soup=BeautifulSoup(wb_text.text,'lxml')
    if soup.select('ul li.js-item a.ft-tit'):
        urls=[b.get('href') for b in soup.select('ul li.js-item a.ft-tit') ]
    else:
        print('这个页面在做select的时候返回空抛弃',channel_url)
        channel_urls.update({'channel_url':channel_url},{'$set':{'crawled':'pageproblem'}})
        return False

    time.sleep(2)
    for a in urls:
        try:
            wb_te=requests.get(a)
        except:
            print('这个页面使用request方法请求出错了，丢弃',a)
            item_urls.insert({'item_url':a,'crawled':'networkproblem'})
            continue
        if 'sorry' in a :
            print('这个网址里含有sorry丢弃')
            continue
        elif 'click' in a and not item_urls.find_one({'item_url':a}):
            item_urls.insert({'item_url':wb_te.url,'crawled':'false'})
            print('已经将插入到item_urls库中了',wb_te.url)
        elif not item_urls.find_one({'item_url':a}):
            item_urls.insert({'item_url':a,'crawled':'false'})
            print('已经将插入到item_urls库中了',wb_te.url)
        time.sleep(2)


def detail_page_spider(item_url):
    #这个函数负责处理每一个商品的详情页，最终得到的商品信息会存储到数据库中
        try:
            #这里用try的原因是因为有时候会出现connection error的错误,所以用这个方法让程序不中断
            wb_text=requests.get(item_url,headers=headers)
        except:
            print('这个页面使用request方法请求出错了，丢弃',item_url)
            item_urls.update({'item_url':item_url},{'$set':{'crawled':'networkproblem'}})
            return False
        if wb_text.status_code == 404 :
            print(item_url,'这个页面不存在了，忽略')
            return False
        else:
            soup = BeautifulSoup(wb_text.text,'lxml')
            a=soup.select('.second-det-infor.clearfix > li:nth-of-type(1)')[0] if  soup.select('.second-det-infor.clearfix > li:nth-of-type(1)') != [] else None
            if a != None:
                a.label.string=''
            data = {
                'title':soup.select('h1.title-name')[0].text if soup.select('h1.title-name') != [] else None,
                'pub_time':soup.select('i.pr-5')[0].text.strip().split(' ')[0] if soup.select('i.pr-5') != [] else None,
                'category':list(soup.select('ul.det-infor > li:nth-of-type(1) > span')[0].stripped_strings) if soup.select('ul.det-infor > li:nth-of-type(1) > span') != [] else None ,
                'price': soup.select('.f22.fc-orange.f-type')[0].text if soup.select('.f22.fc-orange.f-type') != [] else None,
                'area':list(map(lambda x:x.text,list(soup.select('ul.det-infor > li:nth-of-type(3) > a')))) if soup.select('ul.det-infor > li:nth-of-type(3) > a') != [] else None,
                'new_or_old':list(a.stripped_strings) if a != None else None,
                'url':item_url
            }
            if data['title'] != None:
                item_detail_info_db.insert(data)
                print('已经将这条信息插入到数据库',data)
            else:
                print('这条信息里有空值丢弃',data)

            # time.sleep(2)




if __name__ == '__main__':
    get_channel_url_to_db(ganji_channel.get_all_channel(),range(1,1000))
    for i in channel_urls.find({'crawled':'false'},no_cursor_timeout=True):
        # print(time.clock())
        if 'qitawupin' in i['channel_url'] or 'ershoufree' in i['channel_url'] or 'wupinjiaohuan' in i['channel_url'] :
            get_others_commodity_url_to_db(i['channel_url'])
        else:
            url_spider(i['channel_url'])
        channel_urls.update({'_id':i['_id']},{'$set':{'crawled':'true'}})
        # if time.clock() > 5:
        #     continue
#     pool= Pool(processes = 8)
#     pool.map(detail_page_spider,[i['item_url'] for i  in item_urls.find({'crawled':'false'})])
#     pool.close()
#     pool.join()

    for i in item_urls.find({'crawled':'false'},no_cursor_timeout=True):
        detail_page_spider(i['item_url'])
        time.sleep(2)
        item_urls.update({'_id':i['_id']},{'$set':{'crawled':'true'}})




# url='http://bj.ganji.com/jiaju/2041936945x.htm'
# wb=requests.get(url,headers=headers)
# wb.encoding='utf-8'
# soup = BeautifulSoup(wb.text,'lxml')
# print(soup.select('asdasdsa'))

