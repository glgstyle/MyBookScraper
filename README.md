# Configuration :

1. Placez-vous dans le répertoire qui contiendra le projet 
  
2. Récupérer le code venant de GitHub (faire un clone) :

- git clone https://github.com/glgstyle/MyBookScraper.git
- cd MyBookScraper

3. Créer un environnement virtuel : 
- python -m venv env

4. Activer l'environnement : 
- source env/bin/activate 

5. Installer les packages :
- pip install -r requirements.txt
- pip freeze (pour vérifier que les packages se sont bien installés)

# Extraire les infos d'un article

1. Scrapper un article avec scrap_article.py :
- Dans le terminal écrire la ligne de commande python scrap_article.py suivi de l'url de l'article entre quotes  
(exemple : python scrap_article.py "http://books.toscrape.com/catalogue/love-lies-and-spies_622/index.html")
2. Appuyez sur entrée
3. Un fichier article_data.csv s'est crée dans le dossier data comportant les informations du produit(à ouvrir avec excel)

# Extraire tous les produits d'une catégorie
1. Scraper tous les produits d'une catégorie avec scrap_category.py :
- Dans le terminal écrire la ligne de commande python scrap_category.py suivi de l'url de la categorie entre parenthèses  
(exemple : python scrap_category.py "http://books.toscrape.com/catalogue/category/books/fiction_10/")
2. Appuyez sur entrée
3. Un fichier article_data.csv s'est crée dans le dossier data comportant les informations du produit(à ouvrir avec excel)

# Extraire tous les produits de toutes les catégories 
1. Scraper tous les produits de toutes les catégories avec scrap_all_articles_from_all_categories.py :
- Dans le terminal écrire la ligne de commande python scrap_all_articles_from_all_categories.py  
(exemple : python scrap_all_articles_from_all_categories.py)
2. Appuyez sur entrée
3. Dans le dossier data, un dossier categoryCsv s'est crée dans le dossier data comportant les informations du produit(à ouvrir avec excel)

# Extraire tous les produits de toutes les categories

1. Dans le terminal tapper la commande : python scrap_all_articles_from_all_categories.py 
2. Un répertoire nommé categoryCsv s'est crée contenant toutes les informations de tous les livres triés par catégorie

# Extraire les photos des produits

Scraper les photos de toutes les categories avec s :
1. Dans le terminal tapper la commande python scrap_all_articles_from_all_categories.py  
(exemple python scrap_all_articles_from_all_categories.py)
2. Un dossier images s'est crée avec les photos des sites

a faire 

Reformuler le Readme
https://www.markdownguide.org/basic-syntax/
https://www.tutorialspoint.com/python/python_command_line_arguments.htm
ne pas écrire la fonction get all books
recupérer les images a partir de get article infos 