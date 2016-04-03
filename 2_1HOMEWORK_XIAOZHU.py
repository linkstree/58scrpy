import requests
from bs4 import BeautifulSoup
import pymongo
client = pymongo.MongoClient('127.0.0.1',27017)
walden = client['walden']
tab = walden['tab']


# ====================================================== <<<< 设计函数 >>>> =============================================

def get_page_within(pages):
    for page_num in range(1,pages+1):
        wb_data = requests.get('http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(page_num))
        soup = BeautifulSoup(wb_data.text,'lxml')
        titles = soup.select('span.result_title')
        prices = soup.select('span.result_price > i')
        for title, price in zip(titles,prices):
            data = {
                'title':title.get_text(),
                'price':int(price.get_text())
            }
            tab.insert_one(data)
            # print(data)
    print('Done')

get_page_within(3) #获取前三页面得数据
for item in tab.find({'price':{'$gte':500}}):
    print(item)
print(tab)
