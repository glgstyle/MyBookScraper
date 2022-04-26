# Partie3 : Récupération des articles à partir du site en passant par les liens de toutes les catégories
import requests
from bs4 import BeautifulSoup
from tools import get_category_articles_infos


url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup_ul = soup.find('ul', class_='nav')
soup_categories = soup_ul.find_all('li')


# Extract the links of all categories
categories_url = []
category = []
# all_categories_articles_infos = []

for cat in soup_categories:
    cat_url = 'http://books.toscrape.com/' + cat.find('a').get('href')
    categories_url.append(cat_url)
    prepare_category = cat.a.text.replace('\n', '')
    category.append(prepare_category.replace(' ', ''))

# category_name = category[1:-1]

# Find infos for each category in category list
for i in range(1, len(categories_url)):

    # all_books_datas = get_category_articles_infos(categories_url[i])
    get_category_articles_infos(categories_url[i])

    # all_categories_articles_infos.append(all_books_datas)

    # all_infos = data_all_articles
    # with open('category_data.csv', 'w', encoding='utf-8') as category:
    #     w = csv.writer(category, delimiter=',')
    #     w.writerow(header)
    #     for data in range(len(all_infos)):
    #         w.writerow(all_infos[data])
    # line = all_categories_articles_infos
    # for data in category_name[i]:
    # for data in all_categories_articles_infos:
    #
    #     with open("categoryCsv/" + category_name[i] + '.csv', 'w', encoding='utf-8', newline='') as file:
    #         w = csv.writer(file, delimiter=',')
    #         w.writerow(header)
    #         w.writerows(data)
    #         # for data in range(len(all_categories_articles_infos)):
    #         #     # Écrire toutes les données de tous les livres contenus dans une catégorie
    #         #     w.writerow(all_categories_articles_infos[data[i]])


# # i = 0
# # while i < range(len(categories)):
# print(range(len(categories_url)))
# # print(len(categories_url))
#
# # while i in range(len(categories_url) -1):
# # while i in range(categories_url):
# #
# #     # print(categories_url[i])
# #     # get_category_articles_infos(categories_url[i])
# #     i += 1
# #     # print(i)
# #     get_category_articles_infos(categories_url[i])
# #     # print(categories_url[i])
#
# # while i in range(len(categories_url) -1):
#
# for i in range(len(categories_url)):
#
#
#     print(categories_url[i])
#     # print(i)
#
#     # get_category_articles_infos(categories_url[i])
#     # i += 1
#     # print(i)
#     get_category_articles_infos(categories_url[i])
    # print(categories_url[i])

# get_category_articles_infos(categories_url[1])

# pour chacune des categories prendre le lien et chercher les articles de la catégorie
    # for each_cat in range(len(categories_url)):
    # for each_cat in categories_url:
    #
    #       # print(categories_url[each_cat])
    #     all_datas = get_category_articles_infos(categories_url[each_cat])
#         # print(categories_url[each_cat])
#         all_categories_articles_infos.append(all_datas)
#         # print(get_category_articles_infos(prepare_url + categories[each_cat]))
#         # print(categories_url[each_cat])
# print(all_categories_articles_infos)


