# Partie1: Récupération des infos à partir d'un lien article
# Choisissez n'importe quelle page Produit sur le site de Books to Scrape. Écrivez un script Python qui visite cette page et en extrait les informations suivantes :
import sys
import requests
from bs4 import BeautifulSoup
import csv
import os
import urllib.request

# sys.argv -> list arguments passed to the script by the terminal (here the article url)
url = sys.argv[1]
response = requests.get(url)
parser = BeautifulSoup(response.content, 'html.parser')
products_infos = parser.find_all('td')
data = []

# product_page_url
data.append(url)

# universal_product_code (upc)
data.append(products_infos[0].string)

# title
data.append(parser.find('div', class_='product_main').h1.string)

# price_including_tax
price_including_tax = products_infos[3].string
price_tva = price_including_tax.replace('£', '')
data.append(price_tva)

# price_excluding_tax
price_excluding_tax = products_infos[2].string
price_ht = price_excluding_tax.replace('£', '')
data.append(price_ht)

# number_available
data.append(products_infos[5].string)

# product_description
find_p = parser.find_all('p')
data.append(find_p[3].string)

# category
find_a = parser.find_all('a')
data.append(find_a[3].string)

# review_rating
data.append(products_infos[6].string)

# image_url
find_img = parser.find("img")
source = find_img.get('src')
image_url = source.replace("../../", "http://books.toscrape.com/")
data.append(image_url)

# GET images
pictures = []
soup_div_picture = parser.find('div', class_='item active')
soup_picture = soup_div_picture.find('img').get('src')
find_image_url = 'http://books.toscrape.com/' + soup_picture
pictures.append(find_image_url.replace('../../', ''))

# Try to create pictures repertory, if it's not possible(error), dont do anything(continue)
path = 'images/'
try:
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise

# For each picture in pictures, open repertory pictures, copy / paste them inside and refactoring
# their name(picture1, picture2...)
for link in range(len(pictures)):
    img_url = pictures[link]
    print(img_url)
    with open(f'images/image{link + 1}.jpg', 'wb+') as f:
        f.write(urllib.request.urlopen(img_url).read())

# Try to open data, if there is no directory create it
path = 'data'
try:
    os.makedirs(path)
except os.error:
    if not os.path.isdir(path):
        os.mkdir(path)

# Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

with open('data/article_data.csv', 'w', encoding='utf-8') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    w.writerow(data)