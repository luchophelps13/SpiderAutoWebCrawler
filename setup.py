from setuptools import setup, find_packages
import os
from os import path

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SpiderWebCrawler',
  version='0.0.1',
  description='Automatically Scrape Websites',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://upload.pypi.org/legacy/',
  author='Lucas Phillips',
  author_email='Luchcubs23@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='webscraper', 
  packages=find_packages(),
  install_requires=REQUIREMENTS 
)