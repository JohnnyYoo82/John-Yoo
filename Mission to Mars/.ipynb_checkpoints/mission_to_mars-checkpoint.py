#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import dependencies
import pandas as pd
import os
from splinter import Browser
from bs4 import BeautifulSoup


# In[2]:


# Executable path to chrome driver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


# Set url to website being used
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Parse HTML 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[4]:


# Scarpe NASA Mars news for the latest news title and paragraph text and assign them to variables
news_title = soup.find('div', class_='content_title').find('a').text
news_p = soup.find('div', class_='article_teaser_body').text

# Display scrapped data 
print(news_title)
print(news_p)


# ## JPL Mars Space Images - Featured Image

# In[5]:


# Set url to website being used
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Parse HTML 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[6]:


# Scarpe JPL Featured Space for the current Featured Mars Image and assign the url string to a variable
image_url = soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')

# Save a complete url string for this image called featured_image_url
main_url = 'https://www.jpl.nasa.gov'
featured_image_url = main_url + image_url

# Display complete url string for this image
featured_image_url


# ## Mars Weather

# In[7]:


# Set url to website being used
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

# Parse HTML 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[8]:


# Scarpe Mars Weather for the latest Mars weather tweet from the page
# Save the tweet text for the weather report as a variable called mars_weather
mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

# Display data for mars_weather
print(mars_weather)


# ## Mars Facts

# In[9]:


# Set url to website being used
url = 'https://space-facts.com/mars/'
browser.visit(url)

# Scrape the table containing facts about the planet including Diameter, Mass, etc
mars_facts = pd.read_html(url)
mars_facts


# In[10]:


# Use Pandas to convert the data to a HTML table string
mars_facts_df = mars_facts[0]

# Name columns, set index and display data
mars_facts_df.columns = ['Description','Value']
mars_facts_df.set_index('Description', inplace=True)

# Display HTML table string
print(mars_facts_df.to_html())


# ## Mars Hemispheres

# In[11]:


# Set url to website being used
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Parse HTML 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[12]:


# Create list to hold hemisphere dictionaries
hemisphere_image_urls = []

# Find common start for finding hemisphere data
hemispheres = soup.find_all('div', class_='item')

# Create main_url to complete url strings for hemisphere images
main_url = 'https://astrogeology.usgs.gov/'

# Create loop to scrape the Hemisphere title containing the hemisphere name and the image url string for the full resolution hemisphere image
# Use a Python dictionary to store the data using the keys img_url and title.
for hemisphere in hemispheres:
    title = hemisphere.find('h3').text
    hemisphere_url = hemisphere.find('a', class_='itemLink product-item')['href']
    browser.visit(main_url + hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('img', class_='wide-image')['src']
    whole_img_url = main_url + img_url
    hemisphere_image_urls.append({"title" : title, "img_url" : whole_img_url})

# Display the list of hemisphere dictionaries
hemisphere_image_urls

