```python
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import bs4
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

def collectProductData(url):
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'lxml')
    newData = []
    for item in soup.select('.wt-grid__item-xs-6'):
        row = []
        row.append(item.select('h3')[0].get_text().strip())
        
        try:
            row.append(float(item.select('.currency-value')[0].get_text().strip().replace(',','')))
        except:
            # Missing value for sets with no price, append to row IF NO PRICE EXISTS
            row.append(np.nan)
            
        try:
            row.append((float(item.find("input", {'name': "rating"}).attrs['value'])))
        except:
            # Missing value for rating
            row.append(np.nan) 
            
        try:
            review = item.select("span", {"class": "stars-svg stars-smaller"})
            x=([p.getText(strip=True) for p in review])
            y=(''.join(x))
            res = re.findall(r'\(.*?\)', y)
            row.append(int(res[0].replace('(','').replace(')','').replace(',','')))
        except:
            # Missing value for number of ratings
            row.append(np.nan)
            
        try:
            row.append(int(res[2].replace('(','').replace(')','').replace('% off','')))
        except:
            # Missing value for discount
            row.append(0)
        
        newData.append(row)
    newData = pd.DataFrame(newData, columns = ['Product_Name', 'Price_Dollar','Rating_out_of_5','Number_of_Ratings', 'Discount_Percentage'])
    #return newData
    
    # Check if there are more results on the "next" page
    try:
        nextPage = (soup.find("a",{"class":"wt-btn wt-btn--small wt-action-group__item wt-btn--icon"}).attrs['href'])
    except:
        nextPage = None
    
    # If there is another page of results, grab it and combine
    if nextPage:
        return pd.concat([newData, collectProductData(nextPage)], axis=0).reset_index(drop=True)
    # Otherwise return the current data
    else:
        return newData
```


```python
WomenCS=collectProductData("https://www.etsy.com/c/clothing-and-shoes/womens")
MenCS=collectProductData("https://www.etsy.com/c/clothing-and-shoes/mens")
WomenCS.to_csv("WomenCS.csv",index=False)
MenCS.to_csv("MenCS.csv",index=False)
```


```python
WomenCS.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Price_Dollar</th>
      <th>Rating_out_of_5</th>
      <th>Number_of_Ratings</th>
      <th>Discount_Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>15967.000000</td>
      <td>15748.000000</td>
      <td>15748.000000</td>
      <td>15968.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>65.281969</td>
      <td>4.836780</td>
      <td>2969.258001</td>
      <td>5.153432</td>
    </tr>
    <tr>
      <th>std</th>
      <td>169.382743</td>
      <td>0.210758</td>
      <td>5815.805992</td>
      <td>10.569000</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.200000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>18.950000</td>
      <td>4.800000</td>
      <td>331.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>25.000000</td>
      <td>4.889600</td>
      <td>1197.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>52.000000</td>
      <td>4.942400</td>
      <td>2929.000000</td>
      <td>10.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5275.000000</td>
      <td>5.000000</td>
      <td>131195.000000</td>
      <td>70.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
MenCS.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Price_Dollar</th>
      <th>Rating_out_of_5</th>
      <th>Number_of_Ratings</th>
      <th>Discount_Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>16000.000000</td>
      <td>15826.000000</td>
      <td>15826.000000</td>
      <td>16000.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>38.463112</td>
      <td>4.848785</td>
      <td>3142.349615</td>
      <td>4.475313</td>
    </tr>
    <tr>
      <th>std</th>
      <td>123.022331</td>
      <td>0.238634</td>
      <td>5459.143198</td>
      <td>9.651144</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.200000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>15.890000</td>
      <td>4.818200</td>
      <td>260.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>20.440000</td>
      <td>4.892900</td>
      <td>1121.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>28.000000</td>
      <td>4.946100</td>
      <td>3413.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>7875.000000</td>
      <td>5.000000</td>
      <td>55383.000000</td>
      <td>70.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
