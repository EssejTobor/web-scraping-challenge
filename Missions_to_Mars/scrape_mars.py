
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# NASA Mars News
nasa_url = "https://mars.nasa.gov/news/"
browser.visit(nasa_url)


html = browser.html
soup = BeautifulSoup(html, "html.parser")
slide_element = soup.select_one("ul.item_list li.slide")
slide_element.find("div", class_="content_title")


news_title = slide_element.find("div", class_="content_title").get_text()
print(news_title)

news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
print(news_paragraph)


jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)


full_image_button = browser.find_by_id("full_image")
full_image_button.click()
browser.is_element_present_by_text("more info", wait_time=1)
more_info_element = browser.find_link_by_partial_text("more info")
more_info_element.click()


html = browser.html
image_soup = BeautifulSoup(html, "html.parser")


img_url = image_soup.select_one("figure.lede a img").get("src")
img_url

# JPL Mars Space Images

img_url = f"https://www.jpl.nasa.gov{img_url}"
print(img_url)


url_weather = 'https://twitter.com/marswxreport?lang=en'
response_weather = requests.get(url_weather)
soup_weather = BeautifulSoup(response_weather.text, 'lxml')

weather_p = soup_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
print(weather_p)


mars_facts_url = "https://space-facts.com/mars/"
html_table = pd.read_html(mars_facts_url)
html_table[0]


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


hemisphere_image_urls = []

links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    browser.find_by_css("a.product-item h3")[item].click()
    
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]

    hemisphere["title"] = browser.find_by_css("h2.title").text

    hemisphere_image_urls.append(hemisphere)
    
    browser.back()
    
hemisphere_image_urls




