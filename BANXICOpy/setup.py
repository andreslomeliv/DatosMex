# -*- coding: utf-8 -*-
from setuptools import setup

NAME = 'BANXICOpy'
DESCRIPTION = 'Wrap de Python para el API del Sistema de Información Económica del Banco de México'
URL = 'https://github.com/andreslomeliv/DatosMex/tree/master/BANXICOpy'
EMAIL = 'andres.lomeli.v@gmail.com'
AUTHOR = 'Andres Lomelí Viramontes'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

# librerías requeridas
REQUIRED = [
		'requests','pandas'
		]

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=['BANXICOpy'],
	install_requires=REQUIRED,
	license='MIT'
)