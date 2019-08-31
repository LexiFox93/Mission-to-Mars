#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from splinter import Browser
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)    

def scrape():
    browser=init_browser()



# **NASA Mars News**

# In[2]:


    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


    # In[3]:


    page_response = requests.get(url)


    # In[4]:


    soup = BeautifulSoup(page_response.content, "html.parser")
    #print(soup.prettify())


    # In[5]:


    news_title = soup.title.text
    news_title


    # In[6]:


    news_p = soup.p.text
    news_p


    # **JPL Mars Space Images - Featured Image**

    # In[10]:


    #visit website and scrape for featured image
    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(1)
    # click on link to go to new endpoint/site
    browser.click_link_by_id('full_image')
    time.sleep(1)

    # parse html to find link
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_img=soup.find('img', class_='fancybox-image')['src']
    featured_img_url = f'https://www.jpl.nasa.gov{featured_img}'
    print(featured_img_url)


    # In[8]:


    #Use the requests library to download and save img
    import shutil
    response = requests.get(featured_img_url, stream = True)
    with open('img.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


    # In[14]:


    #well...this didn't work...
    #Display the image with Ipython.display
    #from IPython.display import image
    #Image(url='img.jpg')


    # **Mars Weather**

    # In[15]:


    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)


    # In[16]:


    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')
    #print(soup.prettify())


    # In[17]:


    #this worked before then it didn't...sigh
    #newest_tweet=soup.find('div', class_='js-tweet-text-container')
    #print(newest_tweet.text)


    # In[18]:


    html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    print(mars_weather)


    # **Mars Facts**

    # In[19]:


    url = 'https://space-facts.com/mars/'


    # In[20]:


    tables = pd.read_html(url)
    tables


    # In[21]:


    #create datafra,e
    mars_df=tables[0]
    mars_df


    # In[22]:


    #clean df by changing title to Mars Facts and removing Earth data
    mars_df=mars_df.rename(columns={'Mars - Earth Comparison':'Mars Facts'})
    del mars_df['Earth']
    mars_df


    # In[23]:


    #convert to html table string
    mars_df.to_html('Mars Facts.html')
   # 'Mars Facts.html'


    # **Mars Hemispheres**

    # In[33]:


    # use BeautifulSoup to parse website
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())


    # In[32]:


    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Initialize mars_hemi_urls 
    mars_hemi_image_urls = []

    # Store the main_ul 
    mars_hemi_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href'] 
        browser.visit(mars_hemi_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = mars_hemi_url + soup.find('img', class_='wide-image')['src']
        mars_hemi_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
    mars_hemi_image_urls

    browser.quit()

    # In[34]:


    #Use the requests library to download and save img
    import shutil
    response = requests.get(img_url, stream = True)
    with open('img.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


    # In[36]:


    #nope...still doesn't work...
    #Display the image with Ipython.display
    #from IPython.display import image
    #Image(url='img.jpg')


    # In[ ]:




