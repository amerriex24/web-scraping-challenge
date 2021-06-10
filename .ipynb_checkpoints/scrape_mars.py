import os
import csv
import requests
import json
import time
import gmaps
import sqlalchemy
import psycopg2
import pymongo

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from datetime import date
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from matplotlib import style
from scipy import stats
from pprint import pprint
from scipy.stats import linregress
from citipy import citipy
from webdriver_manager.chrome import ChromeDriverManager



pd.options.display.float_format = '{:,.2f}'.format


# %%
# Set up splinter function 
def activate_driver():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path,headless=False)


# %%
#Scraping the Nasa website and converting text to BS 

browser = activate_driver()
browser.visit('https://mars.nasa.gov/news/')
html=browser.html
soup=bs(html, 'html.parser')

#finding news 

news = soup.find_all('div', class_="list_text")[0]

#finding news titles

news_title = news.find(class_="content_title").text


#finding the paragraphs

news_para = news.find(class_="article_teaser_body").text

#date of article

date = news.find(class_='list_date').text


#Dictionary for the scrapped data

final_data = { 
    "News Title": news_title, 
    "News Paragraph": news_para,
    "Date": date
    }

# close browser 
browser.quit()



# %%
print(final_data['News Title'])
print(final_data['News Paragraph'])
print(final_data['Date'])


# %%
##JPL Mars Space Images
##Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.

browser = activate_driver()
browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')



html = browser.html
soup = bs(html, 'html.parser')

mars_image = soup.find('img', class_="headerimage")['src']

mars_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space' + '/' + mars_image

featured_image = {
    "Featured Image Url": mars_url
}


browser.quit()


# %%
featured_image


# %%
##Mars Facts
## Use Pandas web scraper to pull HTML table data into a dataframe

mars_facts_url = 'https://space-facts.com/mars/'

table = pd.read_html(mars_facts_url)
mars_facts_table = pd.DataFrame(table[0])
mars_facts_table = mars_facts_table.rename(columns ={
                                            0:'Descriptions',
                                            1:'Actual Facts'
                                            })

print(mars_facts_table)


# %%
#Creating HTML table 

table_html = mars_facts_table.to_html()

#Clean table 

table_html = table_html.replace('\n', '')

table_html


# %%
##Mars Hemp
## Creating full res images and URLS.
## https://astrogeology.usgs.gov/

mars_hemp_url = 'https://marshemispheres.com/'

browser = activate_driver()
browser.visit(mars_hemp_url)


browser.links.find_by_partial_text('Cerberus Hemisphere Enhanced').click()

html = browser.html
soup = bs(html, 'html.parser')

hemp_title1c = soup.find('h2', class_ = 'title').text
hemp_image1c = soup.find('img', class_ = 'wide-image')['src']
hemp_image1c_url = f'{mars_hemp_url}{hemp_image1c}'
print(hemp_title1c)
print(hemp_image1c_url)

browser.quit()


# %%
browser.visit(mars_hemp_url)



browser.links.find_by_partial_text('Schiaparelli Hemisphere Enhanced').click()

html = browser.html
soup = bs(html, 'html.parser')

hemp_title2s = soup.find('h2', class_ = 'title').text
hemp_image2s = soup.find('img', class_ = 'wide-image')['src']
hemp_image2s_url = f'{mars_hemp_url}{hemp_image2s}'
print(hemp_title2s)
print(hemp_image2s_url)


# %%
browser.visit(mars_hemp_url)


browser.links.find_by_partial_text('Syrtis Major Hemisphere Enhanced').click()

html = browser.html
soup = bs(html, 'html.parser')

hemp_title3sy = soup.find('h2', class_ = 'title').text
hemp_image3sy = soup.find('img', class_ = 'wide-image')['src']
hemp_image3sy_url = f'{mars_hemp_url}{hemp_image3sy}'
print(hemp_title3sy)
print(hemp_image3sy_url)


# %%
browser.visit(mars_hemp_url)



browser.links.find_by_partial_text('Valles Marineris Hemisphere Enhanced').click()

html = browser.html
soup = bs(html, 'html.parser')

hemp_title4v = soup.find('h2', class_ = 'title').text
hemp_image4v = soup.find('img', class_ = 'wide-image')['src']
hemp_image4v_url = f'{mars_hemp_url}{hemp_image4v}'
print(hemp_title4v)
print(hemp_image4v_url)


# %%
#Created a Dictionary to store all data

hemp_final_data = [
    {"title": hemp_title1c, "img_url": hemp_title1c},
    {"title": hemp_title2s, "img_url": hemp_title2s},
    {"title": hemp_title3sy, "img_url": hemp_title3sy},
    {"title": hemp_title4v, "img_url": hemp_title4v},
]

hemp_final_data 


