# -*- coding: utf-8 -*-
from setuptools import setup

NAME = 'INEGIpy'
DESCRIPTION = 'Wrap de Python para los APIs del INEGI'
URL = 'https://github.com/andreslomeliv/DatosMex/tree/master/INEGIpy'
EMAIL = 'andres.lomeli.v@gmail.com'
AUTHOR = 'Andres Lomelí Viramontes'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

# librerías requeridas
REQUIRED = [
		'requests','pandas','matplotlib','seaborn','geopandas','shapely'
		]

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=['INEGIpy'],
	install_requires=REQUIRED,
	license='MIT'
)