from __future__ import unicode_literals
from __future__ import absolute_import

from .modules import standard_search
# from modules import shopping_search

__author__ = "Anthony Casagrande <birdapi@gmail.com>, " + \
    "Agustin Benassi <agusbenassi@gmail.com>"
__version__ = "1.1.0"


"""Defines the public inteface of the API."""

search = standard_search.search

# TODO: This method is not working anymore! There is a new GET
# link for this kind of search
# shopping = shopping_search.shopping

