#Partie 4: téléchargements de toutes les images liées aux articles
# Enfin, prolongez votre travail existant pour télécharger et enregistrer le fichier image de chaque page Produit que vous consultez !
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from tools import search_pagination

# for all books get images, download them and put them in a folder named pictures
def get_images(image_search_url):
    pictures = []
    pagination = search_pagination(image_search_url)
    # loop on every page to find images
    for page in pagination:
        print(page)
        resp = requests.get(page)
        next_soup = BeautifulSoup(resp.content, 'html.parser')
        next_soup_picture = next_soup.find_all('img', class_='thumbnail')
        images = next_soup_picture
        for image in images:
            find_image_url = 'http://books.toscrape.com/' + image.get('src')
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
        with open(f'images/image{link+1}.jpg', 'wb+') as f:
            f.write(urllib.request.urlopen(img_url).read())

get_images("https://books.toscrape.com/catalogue/category/books/fiction_10/")