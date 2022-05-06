# Partie3 : Récupération des articles à partir du site en passant par les liens de toutes les catégories
import requests
from bs4 import BeautifulSoup
from tools import get_category_articles_infos

url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup_ul = soup.find('ul', class_='nav')
soup_categories = soup_ul.find_all('li')
categories_url = []

# For each category in all categories extract the links of all categories, put them in categories_url and
# refactor the name
for cat in soup_categories:
    cat_url = 'http://books.toscrape.com/' + cat.find('a').get('href')
    categories_url.append(cat_url)

# Find all books for each category in category list
for i in range(1, len(categories_url)):
    all_books_infos = get_category_articles_infos(categories_url[i])