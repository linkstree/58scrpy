from bs4 import BeautifulSoup
import requests
import re
import pymongo
client = pymongo.MongoClient('127.0.0.1',27017)#这里定义了mongo的链接方法如需使用请去掉注释
aaa = client['aaa']
tab=aaa['tab']
father_url_breakpoint=aaa['breakpoint']
father_url_page=aaa['father_url_page']
father_url=['http://xa.58.com/changanlu/zufang/pn{}'.format(i) for i in range(1,22)]

father_url_page.find({'fa_url_page':i})