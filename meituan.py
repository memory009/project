import requests
from bs4 import BeautifulSoup
#import time


url='https://www.meituan.com/'
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
res=requests.get(url,headers=header)
print(res.status_code)
bs=BeautifulSoup(res.text,'html.parser')
print(bs)


