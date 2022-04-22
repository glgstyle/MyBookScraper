
import requests
from bs4 import BeautifulSoup
import csv

def get_article_infos(url):

    response = requests.get(url)
    parser = BeautifulSoup(response.content, 'html.parser')
    products_infos = parser.find_all('td')
    data = []


    # print(product_page_url)
    data.append(url)


    # universal_product_code (upc)
    data.append(products_infos[0].string)

    # title
    data.append(parser.find('div', class_='product_main').h1.string)

    # price_including_tax
    price_including_tax = products_infos[3].string
    price_tva = price_including_tax.replace('£', '')
    # print(price_tva)
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
    return data


infos = get_article_infos('http://books.toscrape.com/catalogue/love-lies-and-spies_622/index.html')

# Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax',
          'number_available', 'product_description', 'category', 'review_rating', 'image_url']

with open('article_data2.csv', 'w') as article:
    w = csv.writer(article, delimiter=',')
    w.writerow(header)
    w.writerow(infos)
