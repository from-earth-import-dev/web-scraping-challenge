from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import time

def mars_news():
	# NASA Mars News
	news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	news_browser = Browser('chrome', **executable_path, headless=True)
	titles = []
	blurbs = []

	with news_browser: # Open browser window, extract, close browser window
	    news_browser.visit(news_url)
	    time.sleep(5)
	    html = news_browser.html
	    news_soup = BeautifulSoup(html, 'html.parser')

	    for item in news_soup.find_all('ul', class_='item_list'):
	        for li in item:
	            titles.append(li.find('div', class_='content_title').text)
	            blurbs.append(li.find('div', class_='article_teaser_body').text)

	latest_title = titles[0]
	latest_blurb = blurbs[0]
	news_arr = [latest_title, latest_blurb]

	return news_arr

def mars_images():
	# JPL Mars Space Images - Featured Image
	mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	image_browser = Browser('chrome', **executable_path, headless=True)

	with image_browser:
	    image_browser.visit(mars_image_url)
	    mars_image_html = image_browser.html
	    image_soup = BeautifulSoup(mars_image_html, 'html.parser')

	    for i in image_soup.find_all('article', class_='carousel_item'):
	        background_image = i['style'].split(' ')
	        
	raw_url = background_image[1]
	clean_url = raw_url.split("'")[1].split('spaceimages')[1][1:]
	base_url = mars_image_url.split('?')[0]
	featured_image_url = base_url + clean_url

	return featured_image_url

def mars_weather():
	# Mars Weather
	mars_weather_url = 'https://twitter.com/marswxreport'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	weather_browser = Browser('chrome', **executable_path, headless=True)

	mars_weather_arr = []

	with weather_browser:
	    weather_browser.visit(mars_weather_url)
	    mars_weather_html = weather_browser.html
	    weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

	    for item in weather_soup.find_all('ol', class_='stream-items'):
	        for tweet in item.find_all('div', class_='tweet'):
	            mars_weather_arr.append(tweet.find('p').text)

	latest_weather = mars_weather_arr[0]

	return latest_weather


def mars_facts():
	# Mars Facts, returns HTML table of facts about Mars
	mars_facts_url = 'https://space-facts.com/mars/'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	facts_browser = Browser('chrome', **executable_path, headless=True)

	facts_browser.visit(mars_facts_url)
	facts_html = facts_browser.html

	facts_df = pd.read_html(facts_html, index_col=0)[0]
	# idx = facts_df.index.values
	facts_df_html = facts_df.to_html()

	return facts_df_html


def mars_hemispheres():
	# Mars Hemispheres
	mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	hemisphere_browser = Browser('chrome', **executable_path, headless=True)

	with hemisphere_browser:
	    hemisphere_browser.visit(mars_hemisphere_url)
	    time.sleep(2)
	    mars_hemisphere_html = hemisphere_browser.html
	    hemisphere_soup = BeautifulSoup(mars_hemisphere_html, 'html.parser')

	    hemisphere_image_urls = []

	    for i in hemisphere_soup.find_all('div', class_='results'):
	        for j in i.find_all('div', class_='description'):
	            for a in j.find_all('a'):
	                hemisphere_dict = {}
	                
	                hemisphere_browser.click_link_by_partial_text(a.text)
	                hemisphere_dict['title'] = a.text.split('Enhanced')[0]
	                
	                img_html = hemisphere_browser.html
	                img_soup = BeautifulSoup(img_html, 'html.parser')
	                for item in img_soup.find_all('div', class_='downloads'):
	                    hemisphere_dict['img_url'] = item.find('a').get('href')
	                hemisphere_image_urls.append(hemisphere_dict)
	                time.sleep(1)
	                
	                hemisphere_browser.back()
	                time.sleep(2)
	return hemisphere_image_urls

def scrape():	
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

	news = mars_news()
	images = mars_images()
	weather = mars_weather()
	facts = mars_facts()
	hemi = mars_hemispheres()

	scrape_data = {
		"last_headline": news[0],
		"last_summary": news[1],
		"featured_image": images,
		"weather": weather,
		"mars_facts_html": facts,
		"hemisphere_images": hemi
	}

	return scrape_data