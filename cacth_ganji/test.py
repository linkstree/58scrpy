from bs4 import BeautifulSoup
import requests
url='http://bj.ganji.com/yingyouyunfu/o10/'
wb_text = requests.get(url)
soup = BeautifulSoup(wb_text.text,'lxml')
print(len(soup.select('.next')))
