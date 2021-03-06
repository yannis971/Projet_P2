# -*-coding:utf-8 -*
"""
Module parser avec une classe Parser pour scrapper les données
"""
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import progressbar

from bs4 import BeautifulSoup

from . import parametres

def alim_data(balise_th, balise_td, data):
    """
        Alimentation données produits suite et fin
    """
    if balise_th == "UPC":
        data['universal_product_code'] = balise_td
    if balise_th == "Price (excl. tax)":
        data['price_excluding_tax'] = balise_td
    if balise_th == "Price (incl. tax)":
        data['price_including_tax'] = balise_td
    if balise_th == "Number of reviews":
        data['review_rating'] = balise_td.string
    if balise_th.string == "Availability":
        number_available = ""
        for caractere in balise_td.string:
            if caractere.isdigit():
                number_available += caractere
        if number_available == "":
            number_available = "0"
        data['number_available'] = number_available

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
    def create_beautiful_soup_object(url):
        """
        returns an object BeautifulSoup from a given url
        """
        try:
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
        except HTTPError as ex:
            print("create_beautiful_soup_object Exception HTTPError :", ex)
            print("url =", url)
        except URLError as ex:
            print("create_beautiful_soup_object Exception URLError :", ex)
            print("url =", url)
        except UnicodeDecodeError as ex:
            print("create_beautiful_soup_object Exception UnicodeDecodeError :", ex)
            print("url =", url)
        else:
            return soup

    @staticmethod
    def parse_url(url):
        """
        parse the url given as parameter and
        returns an object parse_result
        """
        try:
            parse_result = urlparse(url)
        except AttributeError as ex:
            # raise
            print("parse_url Exception AttributeError : ", ex)
        else:
            return parse_result

    def parse_product(self, url):
        """
        parse the url given as parameter and
        returns a dict() with the data below :
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
        data = {'product_page_url': url, 'universal_product_code': '', 'title': '',
                'price_including_tax': '', 'price_excluding_tax': '',
                'number_available': '0', 'product_description': '',
                'category': '', 'review_rating': '0', 'image_url': ''}

        soup = self.create_beautiful_soup_object(url)

        if soup:
            data['title'] = soup.h1.string.strip()
            data['image_url'] = 'http://' + parametres.NETLOC + '/' \
            + soup.img.attrs['src'].replace("../", "")
            try:
                balise = soup.find(id="product_description")
                data['product_description'] = balise.find_next_sibling().string.strip()
            except AttributeError as ex:
                print("parse_product Exception : ", ex)
                print("product_page_url : ", url)
            for balise_a in soup.find_all('a'):
                attr_href = balise_a.attrs['href']
                if attr_href.startswith("../category/books/"):
                    data['category'] = balise_a.string
                    break
            for balise_tr in soup.find_all('tr'):
                (balise_th, balise_td) = tuple(balise_tr.findChildren(limit=2))
                alim_data(balise_th.string, balise_td.string, data)
        return data

    def generate_category_id(self, url):
        """
            parses the url given as parameter and
            return a category_id
        """
        path = self.parse_url(url).path.strip()
        position_debut = len(parametres.CATEGORY)
        liste = (path[position_debut:]).split('/')
        return liste[0]

    def parse_category(self, category_id, url):
        """
            parses the url given given as parameter and
            generates an object generator on a list of dict()
            corresponding to the category's products
        """
        # Initialize variables
        current_url = url

        soup = self.create_beautiful_soup_object(current_url)

        results_form = soup.find('form', class_='form-horizontal')
        nombre_produits = int(results_form.find('strong').string)

        i = 0

        print("Parsing category - category_id : {}".format(category_id))

        # Parsing datas of the category
        with progressbar.ProgressBar(max_value=nombre_produits, redirect_stdout=True) \
                as progress_bar:
            while soup:
                for balise_h3 in soup.find_all('h3'):
                    lien = balise_h3.find('a').attrs['href'].replace("../", "")
                    product_url = "http://" + parametres.NETLOC + parametres.PRODUCT + lien
                    yield self.parse_product(product_url)
                    progress_bar.update(i)
                    i += 1
                balise_next = soup.find('li', class_='next')
                if balise_next:
                    lien = balise_next.find('a').attrs['href'].replace("../", "")
                    if lien:
                        current_url = "http://" + parametres.NETLOC + parametres.CATEGORY \
                                      + category_id + '/' + lien
                        soup = self.create_beautiful_soup_object(current_url)
                    else:
                        break
                else:
                    break

    def parse_categories(self, url):
        """
            parses the url given as parameter and
            returns a list of tuples corresponding to the categories
        """
        soup = self.create_beautiful_soup_object(url)
        if soup:
            for balise_a in soup.find_all('a'):
                if balise_a.attrs['href'].startswith(parametres.CATEGORY[1:]):
                    category_url = "http://" + parametres.NETLOC + '/' + balise_a.attrs['href']
                    category_id = self.generate_category_id(category_url)
                    list_of_products = self.parse_category(category_id, category_url)
                    yield category_id, list_of_products
