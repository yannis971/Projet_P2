# -*-coding:utf-8 -*
"""
    Module main qui lance l'application
"""
import time
from app.parametres import URL
from app.application import Application

TIME_DEBUT = time.gmtime()
APP_INSTANCE = Application(URL)
APP_INSTANCE.run()
TIME_FIN = time.gmtime()
print("Debut du traitement le :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_DEBUT))
print("Fin du traitement   le :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_FIN))
