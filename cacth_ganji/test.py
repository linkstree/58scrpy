from bs4 import BeautifulSoup
import requests
url='http://bj.ganji.com/shoujihaoma/o343/'
wb_text = requests.get(url)
soup = BeautifulSoup(wb_text.text,'lxml')
print(soup.select('li a.next span'))
# print(if [] :   print('true'))
