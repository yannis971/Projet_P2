# -*-coding:utf-8 -*

from . import parametres
from .parser import Parser
from .recorder import Recorder


class Product:
    def __init__(self, valeur):
        (self.productPageUrl, self.universalProductCode, self.title,
         self.priceIncludingTax, self.priceExcludingTax, self.numberAvailable,
         self.productDescription, self.category, self.reviewRating, self.imageUrl) = valeur

    def __str__(self):
        return self.universalProductCode + ' ; ' + self.productPageUrl + ' ; ' + self.title + ' ; ' + ' ; ' + self.reviewRating

    def display(self):
        print("=======================================")
        print("Affichage objet Product dans la console")
        print("=======================================")
        print("universalProductCode :", self.universalProductCode)
        print("productPageUrl : ", self.productPageUrl)
        print("title :", self.title)
        print("priceIncludingTax :", self.priceIncludingTax)
        print("priceExcludingTax :", self.priceExcludingTax)
        print("numberAvailable :", self.numberAvailable)
        print("productDescription :", self.productDescription)
        print("category :", self.category)
        print("reviewRating :", self.reviewRating)
        print("imageUrl :", self.imageUrl)



class Application:

    def __init__(self, url):
        self.url = url
        self.runLevel = None
        parse_result = Parser.parseURL(url)
        # Controle de la validité de l'url passée en paramètres
        if not (parse_result and parse_result.netloc == parametres.NETLOC):
            print("impossible de lancer l'application car url invalide : {}".format(url))
        else:
            path = parse_result.path
            self.runLevel = ""
            if path == parametres.SITE:
                self.runLevel = "SITE"
            elif path.startswith(parametres.CATEGORY) and path.endswith(parametres.INDEX_HTML):
                self.runLevel = "CATEGORY"
            elif path.startswith(parametres.PRODUCT) and path.endswith(parametres.INDEX_HTML):
                self.runLevel = "PRODUCT"
            else:
                print("application level undefined")
        self.product = None

    def run(self):
        if self.runLevel:
            if self.runLevel == "PRODUCT":
                self.product = Product(Parser().parseProduct(self.url))
                self.product.display()
                recorder = Recorder(self.url, self.runLevel)
                recorder.saveProduct(self.product)
            elif self.runLevel == "CATEGORY":
                pass
            else:
                pass
        else:
            print("application run level {} not defined".format(self.runLevel))
