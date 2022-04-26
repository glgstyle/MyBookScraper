import requests
from bs4 import BeautifulSoup
import csv
from requests_html import HTMLSession


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


# Search if there is a next page or not and send urls of each page from category in a table
def search_pagination(baseUrl):
# baseUrl = 'http://books.toscrape.com/catalogue/category/books/fiction_10/'
    response = requests.get(baseUrl)
    soup = BeautifulSoup(response.content, 'html.parser')
    session = HTMLSession()
    ulPager = soup.find_all('ul', class_='pager')

    pages = []
    if not ulPager == []:

        r = session.get(baseUrl)
        for html in r.html:
            pages.append(html.url)
    else:
        pages.append(baseUrl)

    return pages

# Find books in category
def get_category_articles_infos(categoryUrl):
    category_response = requests.get(categoryUrl)
    soup = BeautifulSoup(category_response.content, 'html.parser')
    pagination = search_pagination(categoryUrl)
    data_all_articles = find_books_infos_in_category(pagination)

    # Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.
    header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax',
              'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    all_infos = data_all_articles
    category_name = soup.title.text
    split_string = category_name.split(' |', 1)
    substring = split_string[0]
    name_of_category = substring.replace('\n', '')

    with open('categoryCsv/' + name_of_category + '.csv', 'w', encoding='utf-8') as category:
        w = csv.writer(category, delimiter=',')
        w.writerow(header)
        for data in range(len(all_infos)):
            w.writerow(all_infos[data])



# baseUrl ="http://books.toscrape.com/catalogue/category/books/fiction_10/"
# search_pagination(baseUrl)
# pagination = search_pagination(baseUrl)
# # find_books_infos_in_category(pagination)
# dataAllArticles = find_books_infos_in_category(pagination)

# print(dataAllArticles)

