from bs4 import BeautifulSoup
import requests
import re

father_url=['http://xa.58.com/changanlu/zufang/pn{}'.format(i) for i in range(1,2)]
def from_father_get_son(fa_url):
    fin_url=[]
    for i in father_url:
        # print(i)
        wb_text = requests.get(i)
        soup = BeautifulSoup(wb_text.text,'lxml')
        url=soup.select('body > div.conwrap.clearfix > div.content.clearfix > div.listcon > div > dl > dd > h3 > a')
        uuu = [a.get('href').split('?')[0] for a in url]
        fin_url.extend(uuu)
    # while fin_url:
    #         print(i)
    #         fin_url.remove(i)
    return fin_url

def get_url_features(url):
    if 'anju' not in url and 'jing' not in url and 'jump' not in url:
        wb_data=requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        categorys=soup.find_all(class_='f14 titFontArr')
        print(categorys)
        titles = soup.select('body > div.main > div.house-title > h1')
        update_times = soup.select('body > div.main > div.house-title > div > span')
        prices = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li.house-primary-content-li.house-primary-content-fir.clearfix > div > i > em')
        imgs = soup.select('#smainPic')
        # addresses = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li > div')
        addresses = soup.find_all(class_='titFontC')
        a=re.sub(r'\s','',addresses[0].str())
        # for category,title,update_time,price,img,address in zip(categorys,titles,update_times,prices,)
        data = {
            'category':list(categorys[0].str()),
            'titles':titles[0].get_text(),
            'update_time':update_times[0].get_text(),
            'price':prices[0].get_text(),
            'img':imgs[0].get('src'),
            'address':a
        }
        print(data)
url_a=from_father_get_son(father_url)
list(map(get_url_features,url_a))












