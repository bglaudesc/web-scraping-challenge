from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import time
import pandas as pd

def scrape_info():
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    title, par=mars_news(browser)
    return {
        "news_title": title,
        "news_p": par, 
        "featured_image_url": mars_image(browser),
        "mars_weather":  mars_weather(browser),
        "mars_facts":  mars_facts(),
        "hemisphere_image_urls": mar_hem(browser)
    }
    

def mars_news(browser):
    url = 'https://mars.nasa.gov/news'
    browser.visit (url)
    time.sleep(7)
    html = browser.html
    soup = bs(html,"html.parser")
    Text_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    Par = soup.find("div", class_="article_teaser_body").text
    return Text_title, Par

def mars_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit (url)
    time.sleep(2)
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.links.find_by_partial_text("more info").click()
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")
    image = soup.find("img", class_="main_image")["src"]  
    featured_image_url = base_url + image
    return featured_image_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit (url)
    time.sleep(7)
    soup = bs(browser.html,"html.parser")
    Tweets = soup.find_all("span" , class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    def func(Tweet):
        return Tweet.text
    Tweet_function = list(map(func,Tweets))
    search = 'InSight sol'
    result = [text for text in Tweet_function if search in text]
    Tweet_weather = result[0]
    return Tweet_weather

def mars_facts():
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df = df.rename(columns={0:'title' , 1: 'value'})
    mars_facts = df.to_html(classes='table table-striped')
    return mars_facts

def mar_hem(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit (url)
    hemp_count = len(list(browser.find_by_tag("h3")))
    hemisphere_image_urls = []
    for i in range(hemp_count):
        browser.find_by_tag("h3")[i].click()
        html = browser.html
        soup = bs(html,"html.parser")
        hemisphere_image_urls.append({
            "title": soup.find("h2", class_="title").text,
            "image_url": soup.find("div", class_="downloads").find('a')["href"]
        })
           
        browser.back()
    browser.quit()
    return hemisphere_image_urls