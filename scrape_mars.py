#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pymongo


def init_browser():
    #Set up splinter
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', headless = False)

def scrape():
    browser = init_browser()
    mars_news = {}

    #Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    mars_news['news_title'] = news_title
    mars_news['news_p'] = news_p

    #Featured Image
    #get url

    jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl)
    time.sleep(5)

    # find button and click it to search
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)

    browser.click_link_by_text('more info     ')

    img_html = browser.html
    # create a soup object from the html
    soup = BeautifulSoup(img_html, "html.parser")
    img_path = soup.find('figure', class_='lede').find('img')['src']
    featured_image_url = "https://www.jpl.nasa.gov/" + img_path

    mars_news['featured_image_url'] = featured_image_url

    #Mars Weather
    #Grab latest weather tweet from Twitter
    weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather)

    weather_html = browser.html
    soup = BeautifulSoup(weather_html, "html.parser")
    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()

    mars_news['mars_weather'] = mars_weather

    #Mars Facts
    # #Use pandas to read table and convert to html 
    mars_facts_url = 'https://space-facts.com/mars/'
    tables_df = pd.read_html(mars_facts_url)[0]
    tables_df.columns = ["Description", "Value"]
    html_table = tables_df.to_html(header = False, index = False)

    mars_news['mars_facts'] = html_table
    
    #Mars Hemispheres
    #Visit website using Splinter
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, "html.parser")

    #Create empty list to hold urls
    hemisphere_urls = []

    #Find links on page
    hemispheres = soup.find('div', class_="collapsible results").find_all('a')
    
    #Loop through visit all pages and capture full resolution url
    print(hemispheres)
    for hemisphere in hemispheres:
        
        full_image = hemisphere.get('href')
            
        browser.visit("https://astrogeology.usgs.gov/" + full_image)
        time.sleep(5)
        
        #Get title and image url source
        soup_object = BeautifulSoup(browser.html, 'html.parser')
        img_title = browser.find_by_css('h2.title').text
        img_url = ("https://astrogeology.usgs.gov/" + soup_object.find('img', class_='wide-image').get('src'))
    
        # create image dictionary for each image and title
        hemisphere_dict={'title':img_title, 'img_url':img_url}

        hemisphere_urls.append(hemisphere_dict)

        browser.back()

    mars_news["hemispheres"] = hemisphere_urls

    return mars_news


