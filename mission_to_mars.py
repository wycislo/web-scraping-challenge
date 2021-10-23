from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from time import sleep

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

mars_news_site = "https://mars.nasa.gov/news/"

browser.visit(mars_news_site)
html = browser.html
soup = bs(html,'html.parser')

news_title = soup.find_all("div", class_="list_text")
news_title[0]

title= news_title[0].find("div",class_='content_title').get_text()
paragraph = news_title[0].find("div",class_='article_teaser_body').get_text()
print(title)
print(paragraph)


# find featured image
target_site = 'https://spaceimages-mars.com'
browser.visit(target_site)

html = browser.html
soup = bs(html,'html.parser')

#featured_image_url = browser.find_by_partial_text('featured').value
featured_image_url = target_site + soup.find('img', class_='headerimage fade-in')['src']
print(featured_image_url)

hemi_url = 'https://marshemispheres.com'
#parse the landing page, isolate the image links in the item div
hemi_html = browser.html
hemi_soup = bs(hemi_html, "html.parser")
hemi_links = hemi_soup.find_all("div", class_ = "item")

#create a list for the names and image links
hemi_img_urls = []

#loop thru each link and grab the name and full size image
for link in hemi_links:
    #dictionary to hold the name/link pairs
    hemi_dict = {}
    #name is in the h3 text
    img_name = link.find("h3").text
    #link is in each desctiption, a href
    img_link = link.find("div", class_ = "description").a["href"]
    #add the base url
    # link_base = "https://astrogeology.usgs.gov"
    link_base = hemi_url
    visit_link = link_base +"/"+ img_link
    #visit the link
    browser.visit(visit_link)
    #don't go too fast
    time.sleep(5)
    
    #parse the html
    indv_hemi_html = browser.html
    indv_hemi_soup = bs(indv_hemi_html, 'html.parser')
    
    #grab the full image link from wide-image src
    indv_hemi_url = indv_hemi_soup.find("img", class_ = "wide-image")["src"]
    
    #add to dictionary as hemi_img_name, hemi_img_url
    hemi_dict['hemi_img_name'] = img_name
    hemi_dict['hemi_img_url'] = link_base + indv_hemi_url
    hemi_dict['hemi_source_url'] = visit_link
    #put dictionary into hemi_img_urls
    hemi_img_urls.append(hemi_dict)
    browser.back()

browser.quit()