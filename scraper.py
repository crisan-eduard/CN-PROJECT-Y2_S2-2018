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

def scrape_page_mediagalaxy(my_url):

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
        c.execute('''CREATE TABLE Products(Shop text, Product text, Price real, Link text)''')
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

    was_link_except = 0;

    for container in containers:
        brand = container.div.a["title"]  # reference element in page like in a dictionary

        title_container = container.findAll("a", {"class": "Product-name js-ProductClickListener"})
        product_name = title_container[0].text

        price_container = container.findAll("div", {"class": "Price-current"})
        product_price = price_container[0].text

        product_price = housekeeping.remove_letters_from_string(product_price)
        #print(product_price)
        product_price = float(product_price)/100
        try:
            link_container = brand = container.div.a["href"]
        except:
            was_link_except = 1;
        #properties_container = container.findAll("dl", {"class": "Product-specifications"})
        #product_properties = properties_container[0].text

        #create data list
        #data = [(product_name,product_price[:-3],product_properties)]
        #print(data)
        #insert list to db
        if was_link_except == 0:
            c.execute("insert into Products values (?, ?, ?, ?)", ("MEDIAGALAXY",product_name, product_price, link_container))
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

def scrape_page_emag(my_url):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_abs_path = os.path.join(BASE_DIR, "database.db")
    print("path: " + db_abs_path)

    # create db

    # create db file
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
        c.execute('''CREATE TABLE Products(Shop text, Product text, Price real, Link text)''')
    except:
        print("Products table already exists")

    # /create db

    # open connectiomn, grab the page, close connection

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # grabs each product
    containers = page_soup.findAll("div", {"class": "card"})
    was_brand_exception = 0
    was_link_exception = 0
    was_price_conv_excpetion = 0
    for container in containers:
        try:
            brand = container.div.img["alt"]
        except:
            was_brand_exception = 1

        try:
            link_container = container.a["href"]
        except:
            was_link_exception = 1

        price_container = container.findAll("p", {"class": "product-new-price"})
        product_price = price_container[0].text

        product_price = housekeeping.remove_letters_from_string(product_price)
        print(product_price)
        try:
            product_price2 = float(product_price)/100
        except:
            was_price_conv_excpetion = 1

        if was_brand_exception == 0 and was_price_conv_excpetion == 0:
            # reference the alt attribute of the img tag
            c.execute("insert into Products values (?, ?, ?, ?)", ("EMAG", brand, product_price2, link_container))
            conn.commit()
            #print("EMAG")
            #print(brand)
            #print(removedots(product_price[:-6]) + "." + product_price[-6:])
            #print(link_container)


def read_file(filepath):
    file_obj = open(filepath,"r")
    for line in file_obj:
        if "mediagalaxy" in line:
            scrape_page_mediagalaxy(line)
        elif "emag" in line:
            scrape_page_emag(line)


read_file("pages.txt")
#housekeeping.empty_file("results.txt")