from bs4 import BeautifulSoup
import requests

father_url=['http://xa.58.com/changanlu/zufang/pn{}'.format(i) for i in range(1,2)]
def from_father_get_son(fa_url):
    fin_url=[]
    for i in father_url:
        wb_text = requests.get(i)
        soup = BeautifulSoup(wb_text.text,'lxml')
        url=soup.select('body > div.conwrap.clearfix > div.content.clearfix > div.listcon > div > dl > dd > h3 > a')
        uuu = [a.get('href') for a in url]
        fin_url.extend(uuu)
    return fin_url

# print(from_father_get_son(father_url))
# url_a=from_father_get_son(father_url)[0]
def get_url_features(url):
    wb_data=requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    categorys=soup.select('body > div.headerWrap > div > div.headerLeft.pa > span > a')
    titles = soup.select('body > div.main > div.house-title > h1')
    update_times = soup.select('body > div.main > div.house-title > div > span')
    prices = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li.house-primary-content-li.house-primary-content-fir.clearfix > div > i > em')
    imgs = soup.select('#smainPic')
    addresses = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li > div')
    # for category,title,update_time,price,img,address in zip(categorys,titles,update_times,prices,)
    data = {
        'category':categorys[0].get_text(),
        'titles':titles[0].get_text(),
        'update_time':update_times[0].get_text(),
        'price':prices[0].get_text(),
        'img':imgs[0].get('src'),
        'address':addresses[0].get_text()
    }
    print(data)
url_a=from_father_get_son(father_url)[0]
get_url_features(url_a)












