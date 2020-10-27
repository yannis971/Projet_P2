# -*-coding:utf-8 -*
"""
Module application qui décrit la logique de l'application
"""

from . import parametres
from .parser import Parser
from .recorder import Recorder


class Product:
    """
        Class describing a product
    """
    def __init__(self, data):
        self.product_page_url = data['product_page_url']
        self.universal_product_code = data['universal_product_code']
        self.title = data['title']
        self.price_including_tax = data['price_including_tax']
        self.price_excluding_tax = data['price_excluding_tax']
        self.number_available = data['number_available']
        self.product_description = data['product_description']
        self.category = data['category']
        self.review_rating = data['review_rating']
        self.image_url = data['image_url']

    def __str__(self):
        return self.universal_product_code + ' ; ' + self.product_page_url + ' ; ' \
               + self.title + ' ; ' + ' ; ' + self.review_rating

    def display(self):
        """
        Affichage dans la console de l'objet Product
        """
        print("=======================================")
        print("Affichage objet Product dans la console")
        print("=======================================")
        print("universal_product_code :", self.universal_product_code)
        print("product_page_url : ", self.product_page_url)
        print("title :", self.title)
        print("price_including_tax :", self.price_including_tax)
        print("price_excluding_tax :", self.price_excluding_tax)
        print("number_available :", self.number_available)
        print("product_description :", self.product_description)
        print("category :", self.category)
        print("review_rating :", self.review_rating)
        print("image_url :", self.image_url)


class Category:
    """
        Classe describing a category of books
    """
    def __init__(self, category_id):
        self.category_id = category_id
        self.list_of_products = []

    def feed_products(self, list_of_products):
        """
        Alimentation de la liste de produits
        """
        self.list_of_products = [Product(item) for item in list_of_products]

    def display(self):
        """
        Affichage dans la console de l'objet Category
        """
        print("================================================================")
        print("Affichage Category {} dans la console".format(self.category_id))
        print("================================================================")
        for product in self.list_of_products:
            product.display()
        print("================================================================")
        print(" {} products in Category {}".format(len(self.list_of_products), self.category_id))
        print("================================================================")


class Application:
    """
        Class describing the application
    """
    def __init__(self, url):
        self.url = url
        self.run_level = None
        parse_result = Parser.parse_url(url)
        # Controle de la validité de l'url passée en paramètres
        if not (parse_result and parse_result.netloc == parametres.NETLOC):
            print("impossible de lancer l'application car url invalide : {}".format(url))
        else:
            path = parse_result.path
            self.run_level = ""
            if path == parametres.SITE:
                self.run_level = "SITE"
            elif path.startswith(parametres.CATEGORY) and path.endswith(parametres.INDEX_HTML):
                self.run_level = "CATEGORY"
            elif path.startswith(parametres.PRODUCT) and path.endswith(parametres.INDEX_HTML):
                self.run_level = "PRODUCT"
            else:
                print("application level undefined")

    def run(self):
        """
        Methode qui execute l'application
        """
        if self.run_level:
            if self.run_level == "PRODUCT":
                product = Product(Parser().parse_product(self.url))
                #product.display()
                recorder = Recorder(self.url, self.run_level)
                recorder.save_product(product)
            elif self.run_level == "CATEGORY":
                category_id = Parser().generate_category_id(self.url)
                category = Category(category_id)
                category.feed_products(Parser().parse_category(category_id, self.url))
                recorder = Recorder(self.url, self.run_level)
                recorder.save_category(category)
            else:
                list_of_categories = []
                for (category_id, list_of_products) in Parser().parse_categories(self.url):
                    category = Category(category_id)
                    category.feed_products(list_of_products)
                    list_of_categories.append(category)
                recorder = Recorder(self.url, self.run_level)
                recorder.save_categories(list_of_categories)
            self.display_stats(recorder)
        else:
            print("application run level {} not defined".format(self.run_level))

    def display_stats(self, recorder):
        """
            Display the stats of scrapping data process
        """
        print("=============================================================")
        print("Scrapping de l'url :", self.url)
        print("=============================================================")
        print("Nombre de produits     : {}".format(recorder.nombre_produits))
        print("Nombre de catégories   : {}".format(recorder.nombre_categories))
        print("Nombre de fichiers csv : {}".format(recorder.nombre_fichiers_csv))
        print("Nombre d'images        : {}".format(recorder.nombre_images))
        print("=============================================================")
