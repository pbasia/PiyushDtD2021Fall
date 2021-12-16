```python
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
#url = 'https://www.etsy.com/in-en/c/craft-supplies-and-tools/home-and-hobby/woodworking-and-carpentry?ref=catnav-562'
#url='https://www.etsy.com/c/clothing-and-shoes/womens'
#url='https://www.etsy.com/c/clothing/womens-clothing?explicit=1&ref=catfilter_L1'
url='https://www.etsy.com/c/clothing-and-shoes/mens'

response=requests.get(url,headers=headers)

soup=BeautifulSoup(response.content,'lxml')

import pandas as pd
import bs4
for item in soup.select('.wt-grid__item-xs-6'):
        print('----------------------------------------')
        print(item.select('h3')[0].get_text().strip())
        print(item.select('.currency-value')[0].get_text().strip())
        print(item.find("input", {'name': "rating"}).attrs['value'])
        ab=((item.select("p", {"class" :".wt-screen-reader-only"})[1]))
        for span in ab.find_all('span'):
            span.decompose()
        print(ab.get_text().strip())
        print("him")
        
        
```
