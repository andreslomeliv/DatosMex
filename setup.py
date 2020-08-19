# -*- coding: utf-8 -*-
from setuptools import setup

# meta-data de la librería
NAME = 'INEGI'
DESCRIPTION = 'Wrap para el API del INEGI'
URL = ''
EMAIL = ''
AUTHOR = 'ALV'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

# librerías requeridas
REQUIRED = [
		'requests','pandas','matplotlib','pprint','seaborn'
		]

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=['INEGI'],
	install_requires=REQUIRED,
	license='MIT'
)