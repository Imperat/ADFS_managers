ADFS Managers
=============
[![Build Status](https://travis-ci.org/Imperat/ADFS_managers.svg?branch=master)](https://travis-ci.org/Imperat/ADFS_managers)
[![Code Health](https://landscape.io/github/Imperat/ADFS_managers/master/landscape.svg?style=flat)](https://landscape.io/github/Imperat/ADFS_managers/master)
[![Documentation Status](https://readthedocs.org/projects/adfs-managers/badge/?version=latest)](http://adfs-managers.readthedocs.io/en/latest/?badge=latest)

Introduction
------------
This is my own application for manage statistic and
control Association of Street Football of Saratov.

Installation
------------
I recommend you use virtualenv:

`virtualenv .venv --no-site-packages`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`python manage.py migrate`

Before running the project you need to compile some little C
dependencies:

`mkdir bin`

`gcc --shared cpp_extensions/get_points.c -o bin/get_points.so`

`python manage.py runserver 127.0.0.1:8000`

Compile client-side application with:

`npm i && ./node_modules/.bin/webpack`

Also for testing there are additional dependencies:

`pip install -r test-requirements.txt`

`python manage.py test`

Contributing
------------
ADFS Managers is opensource project and I develop it only for
improve my coding skills and make freely help for ADF of Saratov.
I promise that I shan't earn money using this project.
For this reason, if you are interesting, you are free in contributing
for this project. You can create new issue, pull request or write me e-mail in
leliykin@gmail.com or in Telegram "+79603412336".
