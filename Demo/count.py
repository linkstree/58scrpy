# coding=utf8

from bs4 import BeautifulSoup
import requests

headers = {
    'Referer': 'http://sh.58.com/pingbandiannao/25546128380612x.shtml',
}

url = 'http://jst1.58.com/counter?infoid=25546128380612'
wb_data = requests.get(url)
# wb_data = requests.get(url, headers=headers)
print(wb_data.text)
