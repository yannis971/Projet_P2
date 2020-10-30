# -*-coding:utf-8 -*
"""
Module recorder décrivant une classe Recorder pour enregistrer
les données scrappées
"""
import os
import shutil
import urllib
import pandas as pd
from .parser import Parser
from . import parametres

def create_directory(data_path):
    """
        creates a directory to save the datas
        if the directory already exists it is deleted first
    """
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.mkdir(data_path)

class Recorder:
    """
    Class Recorder with methods to save objets ao Application class into csv files
    """

    def __init__(self, url, runLevel):
        path = Parser.parse_url(url).path.strip()
        create_directory(parametres.DATA_DIRECTORY)
        create_directory(parametres.IMG_DIRECTORY)
        self.nombre_produits = 0
        self.nombre_categories = 0
        self.nombre_fichiers_csv = 0
        self.nombre_images = 0
        if runLevel == "PRODUCT":
            position_debut = len(parametres.PRODUCT)
            liste = (path[position_debut:]).split('/')
            self.nom_fichier = parametres.DATA_DIRECTORY + '/' + liste[0] + '.csv'

    def save_product(self, product):
        """
            Saves a product into a csv file
            Download and save the product image
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
        self.nombre_produits += 1
        self.nombre_fichiers_csv += 1
        self.save_image(product.image_url, parametres.IMG_DIRECTORY)

    def save_image(self, image_url, path):
        """
        Downloads and saves the image from an image url given as parameter
        """
        nom_fichier = path + image_url.split('/')[-1]
        urllib.request.urlretrieve(image_url, nom_fichier)
        self.nombre_images += 1
