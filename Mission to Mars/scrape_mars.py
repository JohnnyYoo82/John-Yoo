# Import dependencies
import pandas as pd
import os
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # Executable path to chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Create mars dictionary for mongo
    mars_data = {}
    
    time.sleep(3)
    # Set url to NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Parse HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape NASA Mars news for the latest news title and paragraph text and assign them to variables
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from NASA Mars News
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    
    time.sleep(3)
    # Set url to JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Parse HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape JPL Featured Space for the current Featured Mars Image and assign the url string to a variable
    image_url = soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')

    # Save a complete url string for this image called featured_image_url
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + image_url

    # Dictionary entry from JPL Mars Space Images - Featured Image
    mars_data['featured_image_url'] = featured_image_url

    time.sleep(3)
    # Set url to Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Parse HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape Mars Weather for the latest Mars weather tweet from the page
    # Save the tweet text for the weather report as a variable called mars_weather
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # Dictionary entry from Mars Weather
    mars_data['mars_weather'] = mars_weather

    time.sleep(3)
    # Set url to Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Scrape the table containing facts about the planet including Diameter, Mass, etc
    mars_facts = pd.read_html(url)

    # Use Pandas to convert the data to a HTML table string
    mars_facts_df = mars_facts[0]

    # Name columns, set index and display data
    mars_facts_df.columns = ['Description','Value']
    mars_facts_df.set_index('Description', inplace=True)

    # Dictionary entry from Mars Weather
    mars_facts =  mars_facts_df.to_html()
    mars_data['mars_facts'] = mars_facts

    time.sleep(3)
    # Set url to Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Parse HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create list to hold hemisphere dictionaries
    hemisphere_image_urls = []

    # Find common start for finding hemisphere data
    hemispheres = soup.find_all('div', class_='item')

    # Create main_url to complete url strings for hemisphere images
    main_url = 'https://astrogeology.usgs.gov/'

    # Create loop to scrape the Hemisphere title containing the hemisphere name and the image url string for the full resolution hemisphere image
    # Use a Python dictionary to store the data using the keys img_url and title.
    for hemisphere in hemispheres:
        time.sleep(3)
        title = hemisphere.find('h3').text
        hemisphere_url = hemisphere.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('img', class_='wide-image')['src']
        whole_img_url = main_url + img_url
        hemisphere_image_urls.append({"title" : title, "img_url" : whole_img_url})

    # Dictionary entry from Mars Hemispheres
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    # Populate mars_data dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data
