import time
from get_item_info import item_detail_info_db
from get_item_info import item_urls
while True:
    print('商品详情已经有{}条了'.format(item_detail_info_db.find().count()))
    print('商品详情网址已经有{}'.format(item_urls.find().count()))
    time.sleep(5)