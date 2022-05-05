# Partie2: Récupération de la liste articles à partir d'un lien d'une catégorie

import sys
import requests
import csv
from bs4 import BeautifulSoup
from tools import get_article_infos
from requests_html import HTMLSession
import os

# baseUrl = 'http://books.toscrape.com/catalogue/category/books/fiction_10/'

baseUrl = sys.argv[1]

# Find all books infos in category
def find_books_infos_in_category(pagination):

    allListArticlesNextPages = []
# if there is more than 1 page > loop on every page to find books infos
    if len(pagination) > 1:
        for page in pagination:
            print(page)
            resp = requests.get(page)
            next_soup = BeautifulSoup(resp.content, 'html.parser')
            next_soup_ol = next_soup.find('ol')
            h3s = next_soup_ol.find_all('h3')
    # print(range(len(pagination)))
            for h3 in h3s:
                url = 'http://books.toscrape.com/catalogue' + h3.find('a').get('href')
                url_replace = url.replace('../../..', '')
                info = get_article_infos(url_replace)
                allListArticlesNextPages.append(info)
    return allListArticlesNextPages


# Search if there is a next page or not and send urls of each page from category in a table
def search_pagination(baseUrl):
    response = requests.get(baseUrl)
    soup = BeautifulSoup(response.content, 'html.parser')
    session = HTMLSession()
    ulPager = soup.find_all('ul', class_='pager')

    pages = []
    if not ulPager == []:

        r = session.get(baseUrl)
        for html in r.html:
            pages.append(html.url)
    else:
        pages.append(baseUrl)

    return pages


# Écrivez les données extraites dans un seul fichier CSV:

#  Header for Csv file
header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
          'price_excluding_tax',
          'number_available', 'product_description', 'category', 'review_rating', 'image_url']

pagination = search_pagination(baseUrl)
dataAllArticles = find_books_infos_in_category(pagination)

# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

with open('data/category_data.csv', 'w') as category:
    w = csv.writer(category, delimiter=',')
    w.writerow(header)
    for data in range(len(dataAllArticles)):
        w.writerow(dataAllArticles[data])

 # # GET images
 #    pictures = []
 #    # loop on every page to find images
 #    for page in pagination:
 #        print(page)
 #        resp = requests.get(page)
 #        next_soup = BeautifulSoup(resp.content, 'html.parser')
 #        next_soup_picture = next_soup.find_all('img', class_='thumbnail')
 #        images = next_soup_picture
 #        for image in images:
 #            find_image_url = 'http://books.toscrape.com/' + image.get('src')
 #            pictures.append(find_image_url.replace('../../', ''))
 #
 #            # Try to create pictures repertory, if it's not possible(error), dont do anything(continue)
 #            path = 'images/'
 #            try:
 #                os.makedirs(path)
 #            except OSError:
 #                if not os.path.isdir(path):
 #                    raise
 #
 #    # For each picture in pictures, open repertory pictures, copy / paste them inside and refactoring
 #    # their name(picture1, picture2...)
 #    for link in range(len(pictures)):
 #        img_url = pictures[link]
 #        print(img_url)
 #        with open(f'images/image{link + 1}.jpg', 'wb+') as f:
 #            f.write(urllib.request.urlopen(img_url).read())