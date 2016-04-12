from bs4 import BeautifulSoup
import requests
import re
import pymongo
client = pymongo.MongoClient('127.0.0.1',27017)#这里定义了mongo的链接
cacth_58 = client['cactch_58']
fa_url = cacth_58['fa_url']
son_url = cacth_58['son_url']

father_url=['http://xa.58.com/changanlu/zufang/pn{}'.format(i) for i in range(1,22)]
#这里father_url就是需要爬取的页面，也就是长安区的租房信息用format来构造从第一页到第n页

def from_father_get_son():
#定义这个函数用来从father_url取得son_url,即页面中每条租房信息的url
    # fin_url=[]
    for i in father_url:
        if fa_url.find_one({'fa_url': i}):
            continue
        wb_text = requests.get(i)
        soup = BeautifulSoup(wb_text.text,'lxml')
        for link in soup.select('body > div.conwrap.clearfix > div.content.clearfix > div.listcon > div > dl > dd > h3 > a'):
            a=link.get('href').split('?')[0]
            #获得的url中http://xa.58.com/zufang/25522253586480x.shtml?version=fangchan_list_pc_0003&amp;psid=158560840191353050051259090&amp;entinfo=25522253586480_0"
            #?之后的字符串实际上经测试是可以去掉的，这里用split方法
            if 'clk' not in a and 'jing' not in a and 'anjuke' not in a:
                #这里发现一些不属于58的跳转页面，这里用一个判断来筛选
                # fin_url.append(a)
                son_url.insert({'son_url':a,'crawled':'false'})
        fa_url.insert({'fa_url':i})

def get_url_features():
    for url in son_url.find({'crawled':'false'}):
        wb_data=requests.get(url['son_url'])
        soup = BeautifulSoup(wb_data.text,'lxml')
        categorys='-'.join(i.get_text() for i in soup.select('.titFontC'))
        #由于soup.select('.titFontC')返回的是包含许多span标签的list，所以使用for进行遍历并且将遍历结果使用get_text()之后使用-来连接得到类目
        titles = soup.select('body > div.main > div.house-title > h1')
        update_times = soup.select('body > div.main > div.house-title > div > span')
        prices = soup.select('body > div.main > div.house-info.white-block.clearfix > div.house-primary-content-wrap.fr > ul > li.house-primary-content-li.house-primary-content-fir.clearfix > div > i > em')
        imgs = soup.select('#smainPic')
        addresses = soup.select('.xiaoqu')
        # print(addresses)
        b=re.sub(r'\s','',addresses[0].get_text()) if addresses != [] else 'unknow'
        #地址部分我使用了正则表达式的替换功能，因为get_text()中得到了大量的空白字符，包括换行符，制表符,这里用\s去替换效果很完美

        data = {#每一个字段后面都使用了解析式因为在跑大量数据时，我们肯定不希望中间因为error退出
            'category':categorys if categorys != [] else 'unknow',
            'titles':titles[0].get_text() if titles != [] else 'unknow',
            'update_time':update_times[0].get_text() if update_times != [] else 'unknow',
            'price':prices[0].get_text()if prices != [] else 'unknow',
            'img':imgs[0].get('src') if imgs !=[] else 'unknow',
            'address':b
        }
        print(data)
        son_url.update({'_id': url['_id']},{'$set':{'crawled':'true'}})

from_father_get_son()
get_url_features()


