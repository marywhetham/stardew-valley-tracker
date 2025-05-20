from bs4 import BeautifulSoup
import pandas as pd
import requests

def subcategories(links):
    sub_location_names = []

    for link in links:
        response = requests.get('https://stardewvalleywiki.com' + link.get('href'))
        sub_html = response.text
        sub_soup = BeautifulSoup(sub_html,'html.parser')

        sub_location_links = sub_soup.select("#mw-pages a")

        sub_location_names += list(map(lambda link: link.text, sub_location_links))

    return sub_location_names

def get_locations():
    base_url = 'https://stardewvalleywiki.com/Category:Locations'
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    location_names = soup.select('#mw-pages a')
    location_names = list(map(lambda link: link.text, location_names))
    location_names += subcategories(soup.select('#mw-subcategories a'))

    return list(set(location_names))

def insert_locations(cur):
    locations_names = get_locations()
    sql_string = "INSERT INTO locations(location_name) VALUES (%s);" 
    
    cur.executemany(sql_string, [(name,) for name in locations_names])
