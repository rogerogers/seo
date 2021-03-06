from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from builtins import range
from builtins import object

from .utils import get_html, normalize_query
from bs4 import BeautifulSoup
import re
from unidecode import unidecode


class ShoppingResult(object):

    """Represents a shopping result."""

    def __init__(self):
        self.name = None
        self.link = None
        self.thumb = None
        self.subtext = None
        self.description = None
        self.compare_url = None
        self.store_count = None
        self.price = None


def shopping(query, pages=1):
    results = []
    for i in range(pages):
        url = _get_shopping_url(query, i)
        html = get_html(url)
        if html:
            j = 0
            soup = BeautifulSoup(html)

            products = soup.findAll("div", "sh-dlr__list-result")
            for prod in products:
                res = ShoppingResult()

                h3 = prod.find("h3")
                if h3:
                    a = h3.find("a")
                    if a:
                        res.compare_url = a["href"]
                    res.name = h3.text.strip()

                psliimg = prod.find("div", "sh-dlr__thumbnail")
                if psliimg:
                    img = psliimg.find("img")
                    if img:
                        res.thumb = img["src"]

                f = prod.find("div", "f")
                if f:
                    res.subtext = f.text.strip()

                price = prod.find("span", "Nr22bf")
                if price:
                    res.price = price.text.strip()

                results.append(res)
                j = j + 1
    return results


def _get_shopping_url(query, page=0, per_page=20):
    return "http://www.google.com/search?hl=en&q={0}&tbm=shop&start={1}&num={2}".format(
        normalize_query(query), page * per_page, per_page
    )
