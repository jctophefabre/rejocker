# -*- coding: utf-8 -*-

__license__ = "Apache-2.0"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'rejocker',
      version = '0.2',
      description = 'REst Json mOCK servER',
      long_description = readme(),
      author = 'Jean-Christophe Fabre',
      author_email = 'jean-christophe.fabre@inrae.fr',
      url = 'https://github.com/jctophefabre/rejocker',
      license = 'GPLv3',
      packages = ['rejocker'],
      package_data = {
          'rejocker': ['resources/*']
      },
      include_package_data = True,
      install_requires = [
          'flask'
      ],
      python_requires = '~=3.5',
     )