#Partie 4: téléchargements de toutes les images liées aux articles
# Enfin, prolongez votre travail existant pour télécharger et enregistrer le fichier image de chaque page Produit que vous consultez !
import os

import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
from tools import get_category_articles_infos


# url = 'https://books.toscrape.com/'
url = 'https://books.toscrape.com/catalogue/category/books/business_35/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup_picture = soup.find_all('img', class_='thumbnail')
pictures = []

# for all books get images, download them and put them in a folder named pictures
# split_string = category_name.split(' |', 1)
# substring = split_string[0]
# name_of_category = substring.replace('\n', '')

def get_images():
    for image in soup_picture:
        find_image_url = 'http://books.toscrape.com/' + image.get('src')
        pictures.append(find_image_url.replace('../../', ''))

    # for link in range(len(pictures)):
    #     save_name = pictures[link].replace('http://books.toscrape.com/media/cache/', '')
    #     print(save_name)

    for link in range(len(pictures)):
        img_url = pictures[link]
        save_name = pictures[link].replace('http://books.toscrape.com/media/cache/', '')
        print(img_url)
        # urllib.request.urlretrieve(img_url)
        with open(f'image{link+1}.jpg', 'wb+') as f:
            f.write(urllib.request.urlopen(img_url).read())

        # html = open('/pictures' + save_name, 'w')
        # html.close()
        # f = open('00000001.jpg', 'wb')
        # f.write(urllib.request.urlopen('http://www.gunnerkrigg.com//comics/00000001.jpg').read())
        # f.close()
            # urllib.request.urlretrieve(img_url)
# imgURL = "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"
#
# urllib.request.urlretrieve(imgURL, "D:/abc/image/local-filename.jpg")


get_images()

print(pictures)

