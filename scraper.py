#
#	BASIC WEB SCRAPER
#

import housekeeping
import sqlite3
import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# my_url = 'https://mediagalaxy.ro/electrocasnice-mari/masini-de-spalat-rufe/masini-de-spalat-frontale'
# my_url = 'https://mediagalaxy.ro/laptop-desktop-it/componente/placi-video'

def scrape_page(my_url):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_abs_path = os.path.join(BASE_DIR, "database.db")
    print("path: " + db_abs_path)

    #create db

    #create db file
    if not os.path.isfile(db_abs_path):
        db_file = open(db_abs_path, "w")
    else:
        print("database.db already exists")

    try:
        conn = sqlite3.connect(db_abs_path)
    except:
        print("ERROR connecting to database")
    c = conn.cursor()

    # Create table
    try:
        c.execute('''CREATE TABLE Products(Product text, Price text, Specifications text)''')
    except:
        print("Products table already exists")

    #/create db

     # open connectiomn, grab the page, close connection
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # grabs each product
    containers = page_soup.findAll("div", {"class": "Product"})

    for container in containers:
        brand = container.div.a["title"]  # reference element in page like in a dictionary

        title_container = container.findAll("a", {"class": "Product-name js-ProductClickListener"})
        product_name = title_container[0].text

        price_container = container.findAll("div", {"class": "Price-current"})
        product_price = price_container[0].text

        properties_container = container.findAll("dl", {"class": "Product-specifications"})
        product_properties = properties_container[0].text

        #create data list
        data = [(product_name,product_price[:-3],product_properties)]
        #print(data)
        #insert list to db
        c.execute("insert into Products values (?, ?, ?)", (product_name, product_price, product_properties))
        #c.executemany('INSERT INTO Products VALUES (?,?,?)',data)
        conn.commit()
        #conn.close()

        #housekeeping.append_line_to_file("product_name: " + product_name + "\n", "results.txt")
        #housekeeping.append_line_to_file("product_price: " + product_price + "\n", "results.txt")
        #housekeeping.append_line_to_file("product_properties: " + product_properties + "\n", "results.txt")
        #housekeeping.append_line_to_file("--------------------------------------", "results.txt")
        # print("brand: " + brand + "\n")
        #print("product_name: " + product_name + "\n")
        #print("product_price: " + product_price + "\n")
        #print("product_properties: " + product_properties + "\n")
        #print("--------------------------------------")


def read_file(filepath):
    file_obj = open(filepath,"r")
    for line in file_obj:
        scrape_page(line)

read_file("pages.txt")
#housekeeping.empty_file("results.txt")