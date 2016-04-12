# coding=utf8

from bs4 import BeautifulSoup
import requests

ganji_url = 'http://bj.ganji.com/jiaju/19657160x.htm'
url_58 = 'http://bj.58.com/shouji/25635310844858x.shtml'

wb_data = requests.get(url_58)
# print(wb_data.status_code)
soup = BeautifulSoup(wb_data.text, 'lxml')

title_tag = soup.select('.mainTitle > h1')
if title_tag:
    title = title_tag[0].get_text()
    print(title)
else:
    print('404页面')
