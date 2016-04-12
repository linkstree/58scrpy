# coding='utf8'

import requests, pymongo, time
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
page_list = ganji['page_list']
url_list = ganji['url_list']


def get_links_from(channel, pages, who_sells='o'):
    list_view = '{}{}{}/'.format(channel, str(who_sells), str(pages))
    if page_list.find_one({'page_url': list_view}):
        return
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.select('.js-item'):
        for link in soup.select('.js-item > a'):
            item_link = link.get('href')
            if url_list.find_one({'url': item_link}):
                continue
            url_list.insert_one({'url': item_link, 'crawled': False})
            print(item_link)
        page_list.insert_one({'page_url': list_view})
        print(list_view)
        time.sleep(2)


def get_detail():
    for data in url_list.find({'crawled': False}):
        wb_data = requests.get(data['url'])
        print('process: ', data)
        # 处理数据 ......
        url_list.update({'_id': data['_id']}, {'$set': {'crawled': True}})
        time.sleep(2)

if __name__ == '__main__':
    channel = 'http://bj.ganji.com/jiaju/'
    for i in range(1, 7):
        get_links_from(channel, i)

    # get_detail()

