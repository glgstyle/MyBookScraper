#Partie 4: téléchargements de toutes les images liées aux articles
# Enfin, prolongez votre travail existant pour télécharger et enregistrer le fichier image de chaque page Produit que vous consultez !

import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from tools import search_pagination
import csv


# for all books get images, download them and put them in a folder named pictures
def get_images(image_search_url):
    # url = 'https://books.toscrape.com/'
    # image_search_url = 'https://books.toscrape.com/catalogue/category/books/business_35/index.html'
    response = requests.get(image_search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_picture = soup.find_all('img', class_='thumbnail')
    pictures = []

    # Pour chaque image dans la page, insérer les liens dans le tableau pictures
    for image in soup_picture:
        find_image_url = 'http://books.toscrape.com/' + image.get('src')
        pictures.append(find_image_url.replace('../../', ''))

    # Essayer de créer le dossier images, si ce n'est pas possible(erreur) ne rien faire(continuer)
    path = 'images/'
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # Pour chaque image dans les images, ouvrir le répertoire images copier les images du site
    # et les coller dans images/ en reformatant le nom (image1, image2...)
    for link in range(len(pictures)):
        img_url = pictures[link]
        print(img_url)
        #
        # with open(f'images/image{link+1}.jpg', 'wb+') as f:
        #     f.write(urllib.request.urlopen(img_url).read())
        with open(f'images/image{link+1}.jpg', 'wb+') as f:
            f.write(urllib.request.urlopen(img_url).read())


def get_categories():
    response = requests.get('https://books.toscrape.com/')
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_ul = soup.find('ul', class_='nav')
    soup_categories = soup_ul.find_all('li')
    all_a = []
    categories_url = []
    category_name = []
    # For each category in all categories extract the links of all categories, put them in categories_url
    for cat in soup_categories:
        cat_url = 'https://books.toscrape.com/' + cat.find('a').get('href')
        categories_url.append(cat_url)
    # For each category in ul extract the text of soup, remove blanks around string, save everything to category_name
    # and remove string'books
        all_a = soup_ul.find_all('a')
    for a in all_a:
        substring = a.text
        remove_blanks = substring.strip()
        category_name.append(remove_blanks)
    category_name.remove('Books')

    # name_of_category = substring.replace(' ', '')
    # category_name.append(name_of_category.replace('\n', ''))
    return (categories_url, category_name)

# get_images('https://books.toscrape.com/index.html')

# print(get_categories()[1])
#
#
# Get all images from website (in all categories)
def get_all_images_in_a_category(category):
    # category_response = requests.get(category)
    # soup = BeautifulSoup(category_response.content, 'html.parser')
    # pagination = search_pagination(category)
    # images_in_category = get_images(pagination)
    # print(images_in_category)
    categories = get_categories()[0]
    images_category = []
    for category in range(1, len(categories)):
        search_images = get_images(categories[category])
        images_category.append(search_images)

    return images_category
    # # Find all books for each category in category list
    # for i in range(1, len(categories_url)):
    #     all_books_images = get_images(categories_url[i])
    #
    # return all_books_images

get_all_images_in_a_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html')
# get_all_images_from_categories()
# # get_images(image_search_url)
# # get_all_images_from_categories('https://books.toscrape.com/')
