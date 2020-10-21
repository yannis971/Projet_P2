# -*-coding:utf-8 -*
from app.parametres import url
from app.application import Application
import time
timeDebut = time.gmtime()
appInstance = Application(url)
appInstance.run()
timeFin = time.gmtime()
print("Debut :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", timeDebut))
print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", timeFin))
