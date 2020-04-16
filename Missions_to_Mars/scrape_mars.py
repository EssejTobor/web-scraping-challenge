from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()
    
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)

    time.sleep(1)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    slide_element = news_soup.select_one("ul.item_list li.slide")
 
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()

    browser.quit()

    print(f'Title: {news_title}\nText: {news_paragraph}')

    browser = init_browser()

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    time.sleep(1)
    
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html

    image_soup = BeautifulSoup(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")

    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'

    browser.quit()

    print(featured_image_url)

    browser = init_browser()

    time.sleep(1)
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    response_weather = requests.get(url_weather)
    soup_weather = BeautifulSoup(response_weather.text, 'lxml')
    mars_weather = soup_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
    print(mars_weather)

    browser.quit()

    mars_facts_url = "https://space-facts.com/mars/"

    html_table = pd.read_html(mars_facts_url)

    df_mars_facts = html_table[1]

    df_mars_facts.columns = ['Description', 'Value']

    df_mars_facts.set_index('Description', inplace=True)

    mars_facts = df_mars_facts.to_html(header=True, index=True)

    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    
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


    browser.quit()

    
    mars_data = {}

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph
    mars_data['featured_image_url'] = featured_image_url
    mars_data['mars_weather'] = mars_weather
    mars_data['mars_facts'] = mars_facts
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print("Scrape Complete!!!")

    return mars_data