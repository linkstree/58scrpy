# coding=utf8

from bs4 import BeautifulSoup
import requests

url = 'http://biz.click.ganji.com/bizClick?url=pZwY0jCfsvFJshI6UhGGshPfUiqJpy7JIitQrHmdP1NdnHmkXaOCIAd0njTQrDE3njmvnNc3rNcYrNm1EHTkPHPaPjIAnHELEH0QnNP0njTQgjTknid0njTQPj0krHDdPjDkgjTknHDYgjTknHDOPWNLPHNQPWK0njTQnHDOgjTknHDQrRkknjDQPj60njTQnHF0njTQnHEvnjnkPH91n1Dkn7kknjDzgjTknHD1nRkknj7BpywbpyOMgjTknH70njTQnHbkP1mkrjwxP-qkudkknjDkgjTknRkknjDkgjTknHcznB3QnWb8Pj08nHTLgjTkngKOIA6fUBdzug7dugPY0ztzsWb8nRkknjDdrjw0njTQsH70njTQsH70njTQIyOsUhqLU-wO0AR0njTQPywWuyFWPWbVmymLnBYYuycYsyc1rjcVuWTdnjw-myRbPHwh&v=2'

wb_data = requests.get(url)
print(wb_data.url)
_id = wb_data.url.split('/')[-1].split('x.')[0]
print('id: ', _id)
