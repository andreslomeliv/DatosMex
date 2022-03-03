# -*- coding: utf-8 -*-
from setuptools import setup

# meta-data de la librería
NAME = 'DatosMex'
DESCRIPTION = 'Wrap para los APIs del INEGI y de Banxico'
URL = ''
EMAIL = 'andres.lomeli.v@gmail.com'
AUTHOR = 'ALV'
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
	packages=['INEGIpy', 'BANXICOpy'],
	install_requires=REQUIRED,
	license='MIT'
)
