from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import pymongo

# set up mongo
# Use PyMongo to establish Mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.images

# print(client.list_database_names())

# check if database exists if it does, delete it 
dblist = client.list_database_names()
print(dblist)

if 'mars_db' in dblist:
    print('Database exists')
    db.drop_collection('images')
    print('mars_db dropped')


# news
url = "https://mars.nasa.gov/news/"

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# # Retrieve page with the requests module
# response = requests.get(url)
browser.visit(url)
html = browser.html

# Create BeautifulSoup object; parse with 'html.parser'
news_soup = BeautifulSoup(html, 'html.parser')
nasa_news = news_soup.find("div", class_="list_text")
news_title = nasa_news.find("div", class_="content_title")
print(news_title.get_text())



# find featured image
target_site = 'https://spaceimages-mars.com'
browser.visit(target_site)

html = browser.html
soup = BeautifulSoup(html,'html.parser')

#featured_image_url = browser.find_by_partial_text('featured').value
featured_image_url = target_site + soup.find('img', class_='headerimage fade-in')['src']
#print(featured_image_url)
featured_image_title = target_site + soup.find('h1', class_="media_feature_title").text.strip()

# mars facts
mars_facts = "https://galaxyfacts-mars.com"
mars_series = pd.read_html(mars_facts)
# There are two tables on this page, read the first one
mars_df = mars_series[1]
mars_df.columns = ['Label', 'Mars']
mars_df.set_index('Label', inplace=True)
#drop index.name to avoid funky second index header row
mars_df.index.name=None
# create html version of pandas table
html_table = mars_df.to_html(index=False, header=False, classes="table table-striped")



hemi_url = 'https://marshemispheres.com'
#parse the landing page, isolate the image links in the item div
hemi_html = browser.html
hemi_soup = BeautifulSoup(hemi_html, "html.parser")
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
    indv_hemi_soup = BeautifulSoup(indv_hemi_html, 'html.parser')
    
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


#  # Return results
mission_to_mars ={
    'news_title' : nasa_news.get_text(),
	'summary': news_title.get_text(),
    'featured_image_title': featured_image_title,
    'featured_image': featured_image_url
    
}


collection.insert_one(mission_to_mars)