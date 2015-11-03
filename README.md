Endomondo2TCX
================

Export a your Endomondo workouts to TCX files.

Usage
-----
The script export.py may be used to backup the complete workout history:

    python endomondo2tcx.py

You will be asked for your Endomondo email and password, and then the script will do the rest.

You can insert your credentials in a text file named "endomondo_data.txt" with this content:
 username
 password
 proxy (in case you need it)


Requirements
------------
- Python 2.6+
    - lxml
    - requests


Installing
----------
To set up the requirements for this project, you can install the dependencies by pip.  

First, it's highly recommended to set up a virtualenv:

    virtualenv venv --distribute
    source ./venv/bin/activate

Then install the requirements:

    pip install -r requirements

And you're set!


Authors
-------
This is my personal project [@dtrillo](https://github.com/dtrillo) based on the script created [@yannickcarer](https://github.com/yannickcarer).
