#!/usr/bin/env python

import djangomango
from setuptools import setup, find_packages

setup(
    name=djangomango.__title__,
    version=djangomango.__version__,
    description='More Mango, less Django!',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author=djangomango.__author__,
    author_email='',
    url='https://github.com/pypug/django-mango',
    packages=find_packages(),
    package_data={
        '': ['LICENSE'],
        'djangomango': ['static/*.*', 'templates/*.*']
    },
    include_package_data=True,
    license=open("LICENSE").read(),
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
    scripts=['manage.py'],
)
