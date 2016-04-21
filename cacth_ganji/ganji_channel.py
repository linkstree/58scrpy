from bs4 import BeautifulSoup
import requests
import re
import pymongo

wb_text = requests.get('http://bj.ganji.com/wu/')
wb_text.encoding='utf-8'
soup=BeautifulSoup(wb_text.text,'lxml')
def get_all_channel():
    allcateory_urls = list(map(lambda x:x.get('href'),soup.select('dl.fenlei dt a')))
    all_channel=list(map(lambda x:x.strip('/'),allcateory_urls))
    channel=[]
    for i in all_channel:
        if 'shoujihaoma' not in i:
            channel.append(i)
    return channel

