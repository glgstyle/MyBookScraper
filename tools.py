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

# Find books in category
def get_category_articles_infos(categoryUrl):
    category_response = requests.get(categoryUrl)
    soup = BeautifulSoup(category_response.content, 'html.parser')
    pagination = search_pagination(categoryUrl)
    data_all_articles = find_books_infos_in_category(pagination)

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

    return pictures

# :::::::::::::::::
def get_all_images_in_a_category(category):
    global category_path
    pagination = search_pagination(category)
    all_images_next_page = []

    name_of_category = get_categories()[1]
    path = 'categoryImages/'

    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # loop on every page to find books images
    for page in pagination:
        print(page)
        find_images = get_images(page)
        # print(find_images)
        all_images_next_page.append(find_images)

        for name in name_of_category:
            category_path = path + name
            try:
                os.makedirs(category_path)
            except OSError:
                if not os.path.isdir(category_path):
                    raise
        # For each category add the name of category to the path like: categoryCsv/images/Travel
        # for name in name_of_category:
        for link_image in range(len(all_images_next_page)):
            img_url = all_images_next_page[link_image]
            print(img_url)
            # with open(category_path + "/" + f'image{link_image + 1}.jpg', 'wb+') as f:
            for img in img_url:
                with open('categoryImages' + "/" + f'image{link_image+1}.jpg', 'wb+') as f:
                    print(img)
                    f.write(urllib.request.urlopen(img).read())






    # exit()
        # with open(category_path + "/" + f'image{link + 1}.jpg', 'wb+') as f:
        #     for img in range(len(img_url)):
        #         f.write(urllib.request.urlopen(img).read())


        # for data in range(len(data_all_articles)):
        #     w.writerow(data_all_articles[data])

    return all_images_next_page


def get_all_images_from_all_categories():
    # categories_list = get_categories()[0]
    # images_category = []
    # # Find all books images for each category in category list
    # for category in range(1, len(categories_list)):
    #     search_images = get_all_images_in_a_category(categories_list[category])
    #     images_category.append(search_images)
    # return images_category

    # Try to open categoryCsv/images, if there is no directory images create it
    name_of_category = get_categories()[1]
    link_categories = get_categories()[0]
    # path = 'categoryImages/'

    # path = '\categoryImages'
    #
    # try:
    #     os.makedirs(path)
    # except OSError:
    #     if not os.path.isdir(path):
    #         raise

    # # For each category add the name of category to the path like: categoryCsv/images/Travel
    # for name in name_of_category:
    #     # category_path = path + name
    #     category_path = os.path.join(path, name)
    #
    #     try:
    #         os.makedirs(category_path)
    #     except OSError:
    #         if not os.path.isdir(category_path):
    #             raise

    for link in range(1, len(link_categories)):
        # img_url = link_categories[link]
        get_all_images_in_a_category(link_categories[link])

            # filePath = os.path.join(category_path, f'image{link + 1}')
            # # path_replace = filePath.replace("\", "/")
            # print(filePath)
            # with open(filePath, 'wb+') as f:
            #     f.write(urllib.request.urlopen(img_url).read())
            # # print(path_replace)
            # # with open(category_path + f'image{link+1}.jpg', 'wb+') as f:

    # enregistrer les photos dans le dossier de la categorie

    # exit()
    #
    # # Pour chaque image dans les images, ouvrir le répertoire images copier les images du site
    # # et les coller dans images/ en reformatant le nom (image1, image2...)
    # for link in range(len(pictures)):
    #     img_url = pictures[link]
    #     print(img_url)
    #     with open(f'categoryCsv/+{name_of_category}+images/image{link+1}.jpg', 'wb+') as f:
    #         f.write(urllib.request.urlopen(img_url).read())


# print(get_images('https://books.toscrape.com/catalogue/category/books/business_35/index.html'))
# print(get_images('https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html'))

# get_all_images_in_a_category('https://books.toscrape.com/catalogue/category/books/business_35/index.html')
# get_all_images_in_a_category('https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html')

# get_all_images_from_all_categories()