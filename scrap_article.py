# Partie 1: récupération des infos à partir d'un lien article

# Choisissez n'importe quelle page Produit sur le site de Books to Scrape. Écrivez un script Python qui visite cette page et en extrait les informations suivantes :
import re

import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/love-lies-and-spies_622/index.html'
request = requests.get(url)
parser = BeautifulSoup(request.content, 'html.parser')
data = []


# product_page_url
product_page_url = url
# print(product_page_url)
data.append(product_page_url)


# universal_product_code (upc)
def find_universal_product_code():
    products_infos = parser.find_all('td')
    upc = products_infos[0].string
    # print(upc)
    data.append(upc)

find_universal_product_code()

# title
def find_title():
    t = parser.find('div', class_='product_main').h1
    title = t.string
    data.append(title)

find_title()

# price_including_tax


def find_price_including_tax():

    products_infos = parser.find_all('td')
    price_including_tax = products_infos[3].string
    price_tva = price_including_tax.replace('£', '')
    # print(price_tva)
    data.append(price_tva)

find_price_including_tax()


# price_excluding_tax
def find_price_excluding_tax():

    products_infos = parser.find_all('td')
    price_excluding_tax = products_infos[2].string
    price_ht = price_excluding_tax.replace('£', '')
    data.append(price_ht)


find_price_excluding_tax()


# number_available
def find_number_available():
    products_infos = parser.find_all('td')
    number_available = products_infos[5].string
    data.append(number_available)


find_number_available()


# product_description

def find_description():
    find_p = parser.find_all('p')
    description = find_p[3].string
    data.append(description)


find_description()


# category
def find_category():
    find_a = parser.find_all('a')
    category = find_a[3].string
    data.append(category)


find_category()

# review_rating
def find_review_rating():
    products_infos = parser.find_all('td')
    review_rating = products_infos[6].string
    data.append(review_rating)


find_review_rating()


# image_url
def find_image_url():
    find_img = parser.find("img")
    source = find_img.get('src')
    image_url = source.replace("../../", "http://books.toscrape.com/")
    data.append(image_url)


find_image_url()
# Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

with open('article_data.csv', 'w') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    w.writerow(data)
