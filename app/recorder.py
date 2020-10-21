# -*-coding:utf-8 -*
import pandas as pd

from .application import *
from .parser import Parser


class Recorder:

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
		data = {'product_page_url': [product.productPageUrl,], 
				'universal_ product_code': [product.universalProductCode,],
				'title': [product.title,],
				'price_including_tax': [product.priceIncludingTax,],
				'price_excluding_tax': [product.priceExcludingTax,],
				'number_available': [product.numberAvailable,],
				'product_description': [product.productDescription,],
				'category': [product.category,],
				'review_rating': [product.reviewRating,],
				'image_url': [product.imageUrl,]}
		df = pd.DataFrame(data)
		df.to_csv(self.nomFichier, sep = ';')
