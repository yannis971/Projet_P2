# -*-coding:utf-8 -*
from . import parametres
from .parser import Parser
import pandas as pd


class Recorder:
    """
    Class Recorder with methods to save objets ao Application class into csv files
    """

    def __init__(self, url, runLevel):
        path = Parser.parseURL(url).path.strip()
        if runLevel == "PRODUCT":
            positionDebut = len(parametres.PRODUCT)
            liste = (path[positionDebut:]).split('/')
            self.nomFichier = liste[0] + '.csv'
        elif runLevel == "CATEGORY":
            positionDebut = len(parametres.CATEGORY)
            liste = (path[positionDebut:]).split('/')
            self.nomFichier = liste[0] + '.csv'
        else:
            pass

    def saveProduct(self, product):
        """
            Saves a product into a csv file
        """
        data = {'product_page_url': [product.productPageUrl, ],
                'universal_ product_code': [product.universalProductCode, ],
                'title': [product.title, ],
                'price_including_tax': [product.priceIncludingTax, ],
                'price_excluding_tax': [product.priceExcludingTax, ],
                'number_available': [product.numberAvailable, ],
                'product_description': [product.productDescription, ],
                'category': [product.category, ],
                'review_rating': [product.reviewRating, ],
                'image_url': [product.imageUrl, ]}
        df = pd.DataFrame(data)
        df.to_csv(self.nomFichier, sep=';')

    def saveCategory(self, category):
        """
            Saves a category of products into a csv file
        """

        self.nomFichier = category.categoryId + '.csv'
        data = {'product_page_url': [product.productPageUrl for product in category.listOfProducts],
                'universal_ product_code': [product.universalProductCode for product in category.listOfProducts],
                'title': [product.title for product in category.listOfProducts],
                'price_including_tax': [product.priceIncludingTax for product in category.listOfProducts],
                'price_excluding_tax': [product.priceExcludingTax for product in category.listOfProducts],
                'number_available': [product.numberAvailable for product in category.listOfProducts],
                'product_description': [product.productDescription for product in category.listOfProducts],
                'category': [product.category for product in category.listOfProducts],
                'review_rating': [product.reviewRating for product in category.listOfProducts],
                'image_url': [product.imageUrl for product in category.listOfProducts]}
        df = pd.DataFrame(data)
        df.to_csv(self.nomFichier, sep=';')
