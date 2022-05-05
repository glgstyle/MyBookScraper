# Partie2: Récupération de la liste articles à partir d'un lien d'une catégorie

import sys
import requests
import csv
from bs4 import BeautifulSoup
from tools import get_article_infos
from requests_html import HTMLSession
import os

baseUrl = sys.argv[1]

# Find all books infos in category


def find_books_infos_in_category(pagination):

    allListArticlesNextPages = []
# loop on every page to find books infos
    for page in pagination:
        resp = requests.get(page)
        next_soup = BeautifulSoup(resp.content, 'html.parser')
        next_soup_ol = next_soup.find('ol')
        h3s = next_soup_ol.find_all('h3')
        for h3 in h3s:
            url = 'http://books.toscrape.com/catalogue' + \
                h3.find('a').get('href')
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
