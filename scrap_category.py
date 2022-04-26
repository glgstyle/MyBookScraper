# Partie2: Récupération de la liste articles à partir d'un lien d'une catégorie
import re
import requests
import csv
from bs4 import BeautifulSoup
from tools import get_article_infos, header
from requests_html import HTMLSession


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

# baseUrl = 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/'
# baseUrl = 'http://books.toscrape.com/catalogue/category/books/travel_2/'
baseUrl = 'http://books.toscrape.com/catalogue/category/books/fiction_10/'
response = requests.get(baseUrl)
soup = BeautifulSoup(response.content, 'html.parser')
soup_ol = soup.find('ol')
session = HTMLSession()
dataAllArticles = []



# Search if there is a next page or not and send urls of each page from category in a table
ulPager = soup.find_all('ul', class_='pager')

pagination = []
if not ulPager == []:

    r = session.get(baseUrl)
    for html in r.html:
        pagination.append(html.url)
else:
    pagination.append(baseUrl)
dataAllArticles = find_books_infos_in_category(pagination)


# Écrivez les données extraites dans un seul fichier CSV
with open('category_data.csv', 'w') as category:
    w = csv.writer(category, delimiter=',')
    w.writerow(header)
    for data in range(len(dataAllArticles)):
        w.writerow(dataAllArticles[data])

