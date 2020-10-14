# -*-coding:utf-8 -*
from app.parametres import url
from app.application import Application

appInstance = Application(url)
appInstance.run()