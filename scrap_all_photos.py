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
    response = requests.get(image_search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_picture = soup.find_all('img', class_='thumbnail')
    pictures = []
    pagination = search_pagination(image_search_url)
    # if there is more than one page fin all images on every page

    if len(pagination) > 1:
        for page in pagination:
            print(page)
            for image in soup_picture:
                find_image_url = 'http://books.toscrape.com/' + image.get('src')
                pictures.append(find_image_url.replace('../../', ''))
    # else find image on one page
    else:
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
        with open(f'images/image{link+1}.jpg', 'wb+') as f:
            f.write(urllib.request.urlopen(img_url).read())


get_images("https://books.toscrape.com/catalogue/category/books/classics_6/index.html")