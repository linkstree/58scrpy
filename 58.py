from bs4 import BeautifulSoup
import requests
import re

father_url=['http://xa.58.com/changanlu/zufang/pn{}'.format(i) for i in range(1,22)]
def from_father_get_son(fa_url):
    fin_url=[]
    for i in father_url:
        wb_text = requests.get(i)
        soup = BeautifulSoup(wb_text.text,'lxml')
        for link in soup.select('body > div.conwrap.clearfix > div.content.clearfix > div.listcon > div > dl > dd > h3 > a'):
            a=link.get('href').split('?')[0]
            if 'clk' not in a and 'jing' not in a and 'anjuke' not in a:
                fin_url.append(a)
    return fin_url

def get_url_features(url):
    wb_data=requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    categorys='-'.join(i.get_text() for i in soup.select('.titFontC'))
    # print(categorys)
    titles = soup.select('body > div.main > div.house-title > h1')
    update_times = soup.select('body > div.main > div.house-title > div > span')
    prices = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li.house-primary-content-li.house-primary-content-fir.clearfix > div > i > em')
    imgs = soup.select('#smainPic')
    addresses = soup.select('.xiaoqu')
    # print(addresses)
    b=re.sub(r'\s','',addresses[0].get_text()) if addresses != [] else 'unknow'
    data = {
        'category':categorys if categorys != [] else 'unknow',
        'titles':titles[0].get_text() if titles != [] else 'unknow',
        'update_time':update_times[0].get_text() if update_times != [] else 'unknow',
        'price':prices[0].get_text()if prices != [] else 'unknow',
        'img':imgs[0].get('src') if imgs !=[] else 'unknow',
        'address':b
    }
    print(data)
url_a=from_father_get_son(father_url)
list(map(get_url_features,url_a))
