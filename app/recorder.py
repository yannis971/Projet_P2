# -*-coding:utf-8 -*
"""
Module recorder décrivant une classe Recorder pour enregistrer
les données scrappées
"""
import pandas as pd
from . import parametres
from .parser import Parser


class Recorder:
    """
    Class Recorder with methods to save objets ao Application class into csv files
    """

    def __init__(self, url, runLevel):
        path = Parser.parse_url(url).path.strip()
        if runLevel == "PRODUCT":
            position_debut = len(parametres.PRODUCT)
            liste = (path[position_debut:]).split('/')
            self.nom_fichier = liste[0] + '.csv'
        elif runLevel == "CATEGORY":
            position_debut = len(parametres.CATEGORY)
            liste = (path[position_debut:]).split('/')
            self.nom_fichier = liste[0] + '.csv'
        else:
            pass

    def save_product(self, product):
        """
            Saves a product into a csv file
        """
        data = {'product_page_url': [product.product_page_url, ],
                'universal_ product_code': [product.universal_product_code, ],
                'title': [product.title, ],
                'price_including_tax': [product.price_including_tax, ],
                'price_excluding_tax': [product.price_excluding_tax, ],
                'number_available': [product.number_available, ],
                'product_description': [product.product_description, ],
                'category': [product.category, ],
                'review_rating': [product.review_rating, ],
                'image_url': [product.image_url, ]}
        data_frame = pd.DataFrame(data)
        data_frame.to_csv(self.nom_fichier, sep=';')

    def save_category(self, category):
        """
            Saves a category of products into a csv file
        """

        self.nom_fichier = category.category_id + '.csv'
        data = {'product_page_url': [product.product_page_url
                                     for product in category.list_of_products],
                'universal_ product_code': [product.universal_product_code
                                            for product in category.list_of_products],
                'title': [product.title
                          for product in category.list_of_products],
                'price_including_tax': [product.price_including_tax
                                        for product in category.list_of_products],
                'price_excluding_tax': [product.price_excluding_tax
                                        for product in category.list_of_products],
                'number_available': [product.number_available
                                     for product in category.list_of_products],
                'product_description': [product.product_description
                                        for product in category.list_of_products],
                'category': [product.category
                             for product in category.list_of_products],
                'review_rating': [product.review_rating
                                  for product in category.list_of_products],
                'image_url': [product.image_url
                              for product in category.list_of_products]}
        data_frame = pd.DataFrame(data)
        data_frame.to_csv(self.nom_fichier, sep=';')

    def save_categories(self, list_of_categories):
        """
            Saves a list of categories of products
            Each catgory in its proper csv file
        """
        for category in list_of_categories:
            self.save_category(category)
