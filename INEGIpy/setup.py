 # -*- coding: utf-8 -*-
from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "long_desc.md").read_text(encoding='utf-8')


NAME = 'INEGIpy'
DESCRIPTION = 'Librería en Python para facilitar el uso de las APIs del INEGI'
URL = 'https://github.com/andreslomeliv/DatosMex/tree/master/INEGIpy'
EMAIL = 'andres.lomeli.v@gmail.com'
AUTHOR = 'Andres Lomelí Viramontes'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '2.0.0'

# librerías requeridas
REQUIRED = [
		'requests','pandas','numpy','geopandas','shapely'
		]

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	long_description=README,
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=['INEGIpy'],
	install_requires=REQUIRED,
	license='MIT',
    include_package_data=True,
)