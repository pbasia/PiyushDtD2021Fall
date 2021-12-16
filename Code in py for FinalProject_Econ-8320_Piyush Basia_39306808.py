#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing all the required libraries

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import bs4
import plotly.express as px

# headers is characteristic string that lets servers and network peers identify the application, operating system, vendor, and/or version of the requesting user agent
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

#Function to collect product details by scraping Etsy.com web pages
def collectProductData(url):
    # Retrieve starting URL
    response=requests.get(url,headers=headers)
    # Parse the website with Beautiful Soup
    soup=BeautifulSoup(response.content,'lxml')
    # Create an empty data set
    newData = []
    
    # Iterate over all products listed on the page
    for item in soup.select('.wt-grid__item-xs-6'):
        
        # Create an empty row to fill scraped data
        row = []
        
        # Add the Product name to the row of data
        row.append(item.select('h3')[0].get_text().strip())
        
        try:
            # Extract price and translate to a floating point number from string and removing any ',' from string, append to row IF PRICE EXISTS
            row.append(float(item.select('.currency-value')[0].get_text().strip().replace(',','')))
        except:
            # Missing value for sets with no price, append to row IF NO PRICE EXISTS
            row.append(np.nan)
            
        try:
            # Extract rating and translate to a floating point number from string, append to row IF Rating EXISTS
            row.append((float(item.find("input", {'name': "rating"}).attrs['value'])))
        except:
            # Missing value for rating
            row.append(np.nan) 
            
        try:
            # Extract number of ratings and translate to a floating point number from string, append to row IF Number of Rating EXISTS
            review = item.select("span", {"class": "stars-svg stars-smaller"})
            x=([p.getText(strip=True) for p in review])
            y=(''.join(x))
            res = re.findall(r'\(.*?\)', y)
            row.append(int(res[0].replace('(','').replace(')','').replace(',','')))
        except:
            # Missing value for number of ratings
            row.append(np.nan)
            
        try:
            # Extract Discount Percentage and translate to a floating point number from string, append to row IF Rating EXISTS
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


# In[2]:


#Scraping through Etsy.com clothing-and-shoes section for women and storing the data in WomenCS dataframe
WomenCS=collectProductData("https://www.etsy.com/c/clothing-and-shoes/womens")

#Scraping through Etsy.com clothing-and-shoes section for men and storing the data in MenCS dataframe
MenCS=collectProductData("https://www.etsy.com/c/clothing-and-shoes/mens")


# In[3]:


#Saving the dataFrames to csv files for future use so that we don't have to scrape everytime
WomenCS.to_csv("WomenCS.csv",index=False)
MenCS.to_csv("MenCS.csv",index=False)


# In[5]:


#Getting Details of each numeric column for MenCS dataframe
MenCS.describe()


# In[6]:


#Getting Details of each numeric column for WomenCS dataframe
WomenCS.describe()


# In[7]:


#Adding a column 'Suitable_For' in MenCS dataframe
MenCS['Suitable_For']='Him'


# In[8]:


##Adding a column 'Suitable_For' in WomenCS dataframe
WomenCS['Suitable_For']='Her'


# In[9]:


#Display the dataFrame with first 5 datasets for MenCS
MenCS.head()


# In[10]:


#Display the dataFrame with first 5 datasets for MenCS
WomenCS.head()


# In[11]:


#Dropping any duplicate records and merging Men and Women data into one dataframe named Alldata_CS
Alldata_CS=pd.concat([MenCS, WomenCS], axis=0).drop_duplicates()
Alldata_CS


# In[12]:


#creating a plot to display price variation of products for men and women and saving the figure in fig1
import plotly.express as px
import plotly.graph_objects as go
px.scatter(Alldata_CS,y='Price_Dollar',color='Suitable_For',
          title = "Price analysis of Etsy products: Clothes and Shoes", # update the title of the figure
    labels = { # dictionary for axis labels
        'Price_Dollar' : 'Product Price in $USD', # key should match original label
        'index' : "Product" # value should be new label value)
    })


# In[21]:


# Finding the Product/s from the dataset which has/have the most number of customer ratings
Alldata_CS[Alldata_CS["Number_of_Ratings"] == Alldata_CS.iloc[:,3].max()].reset_index(drop=True)


# In[23]:


# Finding the Product/s from the dataset which has/have the least number of customer ratings
Alldata_CS[Alldata_CS["Number_of_Ratings"] == Alldata_CS.iloc[:,3].min()].reset_index(drop=True)


# In[13]:


#Grouping the Women data on basis of Rating_out_of_5. Using describe() function found that rating min value is 3.0 and highest vaue is 5.0. So interval distributed from 3.0 to 5.0 unevenly. so that we get a proper view of the data.

WPratings=WomenCS.groupby(pd.cut(WomenCS['Rating_out_of_5'],[3,3.5,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5])).count()
WPratings


# In[14]:


#Grouping the Men data on basis of Rating_out_of_5. Using describe() function found that rating min value is 3.0 and highest vaue is 5.0. So interval distributed from 3.0 to 5.0 unevenly. so that we get a proper view of the data.

MPratings=MenCS.groupby(pd.cut(MenCS['Rating_out_of_5'],[3,3.5,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5])).count()
MPratings


# In[15]:


# Creating a dataFrame to store discounted item's count for men and women
discountTable=[['Women',len(WomenCS[WomenCS.Discount_Percentage != 0])], ['Men',len(MenCS[MenCS.Discount_Percentage != 0])]]
Discouts=pd.DataFrame(discountTable,columns=('Discount_For','Discounted_Items_Count'))

#Display Table
Discouts


# In[16]:


#Using describe() function found that Discount_Percentage ranges from 10 to 70 in the dataframe.
#Grouping the Women data on basis of grouped Discount_Percentage. 

aa=WomenCS.groupby(pd.cut(WomenCS['Discount_Percentage'],[10,20,30,40,50,60,70])).count()
aa


# In[17]:


#Using describe() function found that Discount_Percentage ranges from 10 to 70 in the dataframe.
#Grouping the Men data on basis of grouped Discount_Percentage. 

ab=MenCS.groupby(pd.cut(MenCS['Discount_Percentage'],[10,20,30,40,50,60,70])).count()
ab


# In[18]:


#ploting Discount_Percentage data for men and women to find any trendline is Discount Percentages at etsy.com

fig1=aa['Discount_Percentage'].plot(x="Discount_Percentage")
fig2=ab['Discount_Percentage'].plot(x="Discount_Percentage")

