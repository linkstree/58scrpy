from bs4 import BeautifulSoup
import requests
import re

wb_text = requests.get('http://bj.58.com/shoujihao/')
soup = BeautifulSoup(wb_text.text,'lxml')
titles  = soup.select(' a.t > strong')

print(titles)


