#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloads color images of public domain books on Google Books.
(Does not work with copyrighted books!)
(Tested on Linux and Windows.)

When you open a book on Google Books, the color images of the pages are
requested and downloaded dynamically depending on the page you are looking at.

This script starts a browser instance (using Selenium) and opens the book.
Then the script scrolls through the entire book by pressing "page down". On 
each page, the script searches for the image file (using Beautiful Soup), downloads
the color image (using requests) and saves it in a predefined target folder. 

Having started the script, a new window with a browser instance pops up and 
opens the book on Google Books. You can make sure that everything is correct.
The script waits here and asks you in the console to start the download process.
After entering "y", the Python script scrolls through the book and performs all 
the steps described above. You can check the status on the command line. 

At the beginning of the script, you have to specify an (existing) target folder, 
the ID of the book on Google Books. You can find the ID by opening the book 
you want to download and by looking at the URL of the page. (This does not work
with the new Google Books interface. Make sure you use the old one!) You will see 
something like this:
    https://books.google.de/books?id=oihSAAAAcAAJ&pg=PA6 ...
                                     ^^^^^^^^^^^^ ^^^^^^
                               THIS is the ID! /   \ THIS is the page.

If you want to start the download at a specific page, you can define the 
starting page according to the "pg" attribute in the URL (see above), and 
a page to end.

Abort the script by pressing Ctrl-c several times (in the console).

Depending on your internet connection, your operating system, and the Selenium
webdriver you use (Edge, Firefox, or Chrome), the download
will take quite a lot of time (30min++ on Windows with IE).

FAQ: The script can't find the "geckodriver" (or "edgedriver" etc.)! – The 
geckodriver is an executable that is used by Selenium to start a browser. This 
executable has to be downloaded separately. Cf. URLs to download different drivers
in the docs: https://selenium-python.readthedocs.io/installation.html#drivers
Unpack and store the executable in a folder within the project directory.
Store this path in the corresponding variable below (GECKO_PATH, EDGE_PATH, etc.).
The script will use these variables to initialize the driver:
    driver = webdriver.Firefox(executable_path=GECKO_PATH)

Created on Wed June 30 2021

@author: Markus Müller, Institute for European History, Mainz (Germany)

"""
import os
import re
import platform
import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

## Define the basic variables
## Example URL: https://books.google.de/books?id=rV1KAAAAcAAJ&hl=de&pg=PP7#v=onepage&q&f=false
target_folder = "Wild1550-Joh"
book_id = "rV1KAAAAcAAJ"
start = "pg=PP7"
end = "PR1" # or None if you want to download the entire book

## Select and load the webdriver for Selenium, depending on the operating system:
## Get help on https://selenium-python.readthedocs.io/installation.html
if platform.system() == "Windows":
    EDGE_PATH = './edgedriver/msedgedriver.exe' # on Windows, you need to specify the filename!
    driver = webdriver.Edge(executable_path=EDGE_PATH)
elif platform.system() == "Linux":
    GECKO_PATH = './geckodriver'
    driver = webdriver.Firefox(executable_path=GECKO_PATH)

## Pre-process the variables and build the URL:
google_books = "https://books.google.de/books?id="
books_url = google_books + book_id + "&" + start + "&hl=de#v=onepage&q&f=false"
target_folder = str(Path("./" + target_folder))
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

## Define some variables for the loop below:
pattern_page = re.compile(r'pg=(.*?)\&')
pattern_width = re.compile(r'w=\d\d\d\d')
image_urls = {}
page_nr = 0
end_of_book_counter = 0
breaker = False

def save_img(address, filename):
    """ Helper function to download and save an image file. """
    img = requests.get(address)
    open(filename, 'wb').write(img.content)

## Get ready:
driver.get(books_url)
htmlElem = driver.find_element_by_tag_name('html')

user_permission = input("Ready? (y/n) ")
if user_permission == "y":
    ## Let's go!!
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        for div in soup.findAll("div", "pageImageDisplay"):
            for img in list(div.findAll("img")):
                image_url = img.get("src")
                if image_url:
                    page = re.findall(pattern_page, image_url)
                    if page:
                        page = page[0]
                        if page not in image_urls:
                            end_of_book_counter = 0
                            page_nr += 1
                            image_urls[page] = image_url
                            image_url = re.sub(pattern_width, 'w=2500', image_url)
                            filename = book_id + "," + "{:0>4d}".format(page_nr) + "," + page + ".jpeg"
                            filename = str(Path(target_folder, filename))
                            save_img(image_url, filename)
                            print("{:0>4d}".format(page_nr), page, image_url)
                        else:
                            end_of_book_counter += 1
                            if end_of_book_counter > 20:
                                print("Pressed PAGE_DOWN", str(end_of_book_counter), "times but did not find any new pages:")
                                print("Aborting now.")
                                breaker = True
                    else:
                        page_nr += 1
                        print("Skipping unvisible page", page_nr)
                if end:
                    if page == end:
                        print(f"Aborting now because you defined page {end} as the last page.")
                        breaker = True
        
        if breaker:
            break                
        time.sleep(0.100)
        htmlElem.send_keys(Keys.PAGE_DOWN)
else:
    print("Aborted by user.")
