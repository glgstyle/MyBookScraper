Sur votre machine :
- Créer un répertoire pour le projet : 
    - mkdir myBookScrapper
  
- Récupérer le code venant de GitHub (faire un clone) :

    - git clone https://github.com/glgstyle/MyBookScraper.git

- Créer un environnement virtuel : 
    - python -m venv env

- Activer l'environnement : 
    - source env/bin/activate 

- Installer les packages :
    - pip install -r requirements.txt

- pip freeze pour vérifier que les packages se sont bien installés

****Extraire les infos d'une page produit****

- Dans le fichier scrap_article.py :
   - Coller l'url du produit à scarper dans la variable url =
   - Lancer le programme avec la commande :
        - python scrap_article.py
   - Un fichier article_data.csv s'est crée comportant les informations du produit (à ouvrir avec excel)
   
****Extraire tous les produits d'une catégorie****

- Dans le fichier scrap_category.py :
    - Remplacer la variable baseUrl par l'url de la catégorie à extraire
    - le fichier catégorie_data.csv s'est crée avec les informations de tous les produits de la catégorie (à ouvrir avec excel)
- 