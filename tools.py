import os
import requests
from bs4 import BeautifulSoup
import csv
from requests_html import HTMLSession
import urllib.request


def get_article_infos(url):
    response = requests.get(url)
    parser = BeautifulSoup(response.content, 'html.parser')
    products_infos = parser.find_all('td')
    data = []

    data.append(url)

    # universal_product_code (upc)
    data.append(products_infos[0].string)

    # title
    title = parser.find('div', class_='product_main').h1.string
    data.append(title)

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

    # GET images

    soup_div_picture = parser.find('div', class_='item active')
    soup_picture = soup_div_picture.find('img').get('src')
    find_image_url = 'http://books.toscrape.com/' + soup_picture
    picture = find_image_url.replace('../../', '')

    # Try to create pictures repertory, if it's not possible(error), dont do anything(continue)
    path = 'images/'
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # For each picture in pictures, open repertory pictures, copy / paste them inside and refactoring
    # their name(picture1, picture2...)

    with open(f'images/image{title}.jpg', 'wb+') as f:
        f.write(urllib.request.urlopen(picture).read())

    return data


# Find all books infos in a category
def find_books_infos_in_category(pagination):
    all_list_articles_next_page = []
    # loop on every page to find books infos
    for page in pagination:
        print(page)
        resp = requests.get(page)
        next_soup = BeautifulSoup(resp.content, 'html.parser')
        next_soup_ol = next_soup.find('ol')
        h3s = next_soup_ol.find_all('h3')
        for h3 in h3s:
            url = 'http://books.toscrape.com/catalogue' + h3.find('a').get('href')
            url_replace = url.replace('../../..', '')
            info = get_article_infos(url_replace)
            all_list_articles_next_page.append(info)
    return all_list_articles_next_page


# Search if there is a next page or not and send urls of each page from category in a table
def search_pagination(baseUrl):
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

# Get categories url and categories name
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
    # and remove string books
        all_a = soup_ul.find_all('a')
    for a in all_a:
        substring = a.text
        remove_blanks = substring.strip()
        category_name.append(remove_blanks)
    category_name.remove('Books')

    # name_of_category = substring.replace(' ', '')
    # category_name.append(name_of_category.replace('\n', ''))
    return (categories_url, category_name)

# Find books in category
def get_category_articles_infos(categoryUrl):
    category_response = requests.get(categoryUrl)
    soup = BeautifulSoup(category_response.content, 'html.parser')
    pagination = search_pagination(categoryUrl)
    data_all_articles = find_books_infos_in_category(pagination)

    # # GET images
    # pictures = []
    # # loop on every page to find images
    # for page in pagination:
    #     print(page)
    #     resp = requests.get(page)
    #     next_soup = BeautifulSoup(resp.content, 'html.parser')
    #     next_soup_picture = next_soup.find_all('img', class_='thumbnail')
    #     images = next_soup_picture
    #     for image in images:
    #         find_image_url = 'http://books.toscrape.com/' + image.get('src')
    #         pictures.append(find_image_url.replace('../../', ''))
    #
    #         # Try to create pictures repertory, if it's not possible(error), dont do anything(continue)
    #         path = 'images/'
    #         try:
    #             os.makedirs(path)
    #         except OSError:
    #             if not os.path.isdir(path):
    #                 raise
    #
    # # For each picture in pictures, open repertory pictures, copy / paste them inside and refactoring
    # # their name(picture1, picture2...)
    # for link in range(len(pictures)):
    #     img_url = pictures[link]
    #     print(img_url)
    #     with open(f'images/image{link + 1}.jpg', 'wb+') as f:
    #         f.write(urllib.request.urlopen(img_url).read())
    #
    #  Header for Csv file
    header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax',
              'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    category_name = soup.title.text
    split_string = category_name.split(' |', 1)
    substring = split_string[0]
    name_of_category = substring.replace('\n', '')

    # Try to open categoryCsv, if there is no directory create it
    path = 'categoryCsv'
    try:
        os.makedirs(path)
    except os.error:
        if not os.path.isdir(path):
            os.mkdir(path)

    # Open categoryCsv and write all datas(header + datas) from all books on the website
    with open('categoryCsv/' + name_of_category + '.csv', 'w', encoding='utf-8') as category:
        w = csv.writer(category, delimiter=',')
        w.writerow(header)
        for data in range(len(data_all_articles)):
            w.writerow(data_all_articles[data])

