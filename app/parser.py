# -*-coding:utf-8 -*
from urllib.parse import urlparse

from urllib.request import urlopen

from bs4 import BeautifulSoup

from . import parametres


class Parser:
    """
        Class with methods to parse an URL and different objects on Application class such as
        Product
        Category
        Categories
    """

    def __init__(self):
        pass

    @staticmethod
    def createBeautifulSoupObject(url):
        """
        returns an object BeautifulSoup from a given url
        """
        try:
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            # raise
            print("createBeautifulSoupObject Exception : ", e)
        else:
            return soup

    @staticmethod
    def parseURL(url):
        """
        parse the url given as parameter and
        returns an object ParseResult
        """
        try:
            parseResult = urlparse(url)
        except Exception as e:
            # raise
            print("parseURL Exception : ", e)
        else:
            return parseResult

    def parseProduct(self, url):
        """
        parse the url given as parameter and
        return a tuple with the data below :
        product_page_url
        universal_ product_code (upc)
        title
        price_including_tax
        price_excluding_tax
        number_available
        product_description
        category
        review_rating
        image_url
        """
        # Initialize variables
        product_page_url = url
        universal_product_code = ""
        title = ""
        price_including_tax = ""
        price_excluding_tax = ""
        number_available = "0"
        product_description = ""
        category = ""
        review_rating = "0"
        image_url = ""

        soup = self.createBeautifulSoupObject(url)

        if soup:
            title = soup.h1.string.strip()
            image_url = parametres.NETLOC + '/' + soup.img.attrs['src'].replace("../", "")
            product_description = soup.find(id="product_description").find_next_sibling().string.strip()
            for balise_a in soup.find_all('a'):
                attr_href = balise_a.attrs['href']
                if attr_href.startswith("../category/books/"):
                    category = balise_a.string
                    break
            for balise_tr in soup.find_all('tr'):
                (balise_th, balise_td) = tuple(balise_tr.findChildren(limit=2))
                if balise_th.string == "UPC":
                    universal_product_code = balise_td.string
                elif balise_th.string == "Price (excl. tax)":
                    price_excluding_tax = balise_td.string
                elif balise_th.string == "Price (incl. tax)":
                    price_including_tax = balise_td.string
                elif balise_th.string == "Number of reviews":
                    review_rating = balise_td.string
                elif balise_th.string == "Availability":
                    number_available = ""
                    for caractere in balise_td.string:
                        if caractere.isdigit():
                            number_available += caractere
                    if number_available == "":
                        number_available = "0"
        return (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                number_available, product_description, category, review_rating, image_url)

    def parseCategory(self, url):
        pass

    def parseCategories(self, url):
        pass
