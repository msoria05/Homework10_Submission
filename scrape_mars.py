# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from flask import Flask, render_template
import pymongo
from time import sleep

# Initialize browser
def init_browser():
    # Chromedriver path
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create empty dictionary to hold Mars Info
mars_info = {}

sleep(0.5) # Time in seconds

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the NASA Mars News Site
        NASA_url = "https://mars.nasa.gov/news/"
        browser.visit(NASA_url)

        # Create an HTML object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, "html.parser")

        # Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
        news_title = soup.find("div", class_= "content_title").find("a").text
        news_p = soup.find("div", class_="article_teaser_body").text

        news_title = soup.find("div", class_= "content_title").find("a").text
        news_p = soup.find("div", class_="article_teaser_body").text

        # Dictionary entry from MARS NEWS
        mars_info["news_title"] = news_title
        mars_info["news_p"] = news_p

        return mars_info

    finally:

        browser.quit()

sleep(0.5) # Time in seconds

# FEATURED IMAGE
def scrape_mars_image():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the url for JPL Featured Space Image
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)

        # Create an HTML object
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')

        # Format image url by replacing unnecessary elements
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Main Url 
        main_url = "https://www.jpl.nasa.gov"

        # Concatenate website main url with featured image url
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info["featured_image_url"] = featured_image_url 
        
        return mars_info

    finally:

        browser.quit()

sleep(0.5) # Time in seconds        

# MARS WEATHER 
def scrape_mars_weather():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the Mars Weather twitter account
        weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)    

        # Create an HTML object
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_weather, "html.parser")

        # Scrape the latest Mars weather tweet from the page
        tweets = soup.find_all("div", class_="js-tweet-text-container")

        # Look for weather related tweet and save the tweet text for the weather report as a variable called mars_weather
        for tweet in tweets: 
            mars_weather = tweet.find("p").text
            if "Sol" and "pressure" in mars_weather:
                print(f"Mars Weather Tweet: \n{mars_weather}")
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info["mars_weather"] = mars_weather
        
        return mars_info

    finally:

        browser.quit()

sleep(0.5) # Time in seconds

# MARS FACTS
def scrape_mars_facts():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the Mars Facts webpage
        mars_facts_url = "https://space-facts.com/mars/"

        # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
        mars_facts_db = pd.read_html(mars_facts_url)[0]

        # Assign column names and set index
        mars_facts_db.columns = ["Description", "Mars Value", "Earth Values"]
        mars_facts_db.set_index("Description", inplace=True)

        # Display database table
        mars_facts_db

        # Use Pandas to convert the data to a HTML table string.
        data = mars_facts_db.to_html()

        # Dictionary entry from MARS FACTS
        mars_info["mars_facts"] = data

        return mars_info

    finally:

        browser.quit()

sleep(0.5) # Time in seconds

# MARS HEMISPHERES
def scrape_mars_hemispheres():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres
        mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(mars_hemispheres_url)    

        # Create an HTML object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, "html.parser")

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all("div", class_="item")

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Obtain high resolution images for each of Mar's hemispheres
        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find("h3").text
            
            # Links to the hemispheres to find the image url to the full resolution image
            base_img_url = i.find("a", class_="itemLink product-item")["href"]
            
            # Link to Main URL 
            hemispheres_main_url = "https://astrogeology.usgs.gov"
            
            # Visit full image website 
            browser.visit(hemispheres_main_url + base_img_url)
            
            # Create HTML Object 
            base_img_html = browser.html
            
            # Parse HTML with Beautiful Soup 
            soup = bs(base_img_html, "html.parser")
    
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find("img", class_="wide-image")["src"]
            
            # Append the dictionary with the image url string and the hemisphere title to a list.  
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        # Dictionary entry from MARS HEMISPHERES
        mars_info["hemisphere_image_urls"] = hemisphere_image_urls

        return mars_info

    finally:

        browser.quit()

    