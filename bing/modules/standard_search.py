from __future__ import unicode_literals
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
from .utils import _get_search_url, get_html
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import unquote, parse_qs, urlparse, urljoin
from unidecode import unidecode
from re import match, findall


class BingResult(object):

    """Represents a google search result."""

    def __init__(self):
        self.name = None  # The title of the link
        self.link = None  # The external link
        self.google_link = None  # The google link
        self.description = None  # The description of the link
        self.thumb = None  # Thumbnail link of website (NOT implemented yet)
        self.cached = None  # Cached version link of page
        self.page = None  # Results page this one was on
        self.index = None  # What index on this page it was on
        self.number_of_results = None # The total number of results the query returned

    def __repr__(self):
        name = self._limit_str_size(self.name, 55)
        description = self._limit_str_size(self.description, 49)

        list_google = ["BingResult(",
                       "name={}".format(name), "\n", " " * 13,
                       "description={}".format(description)]

        return "".join(list_google)

    def _limit_str_size(self, str_element, size_limit):
        """Limit the characters of the string, adding .. at the end."""
        if not str_element:
            return None

        elif len(str_element) > size_limit:
            return unidecode(str_element[:size_limit]) + ".."

        else:
            return unidecode(str_element)


# PUBLIC
def search(word, num=4):
    """Returns a list of GoogleResult.

    Args:
        query: String to search in google.
        pages: Number of pages where results must be taken.
        area : Area of google homepages.
        first_page : First page.

    TODO: add support to get the google results.
    Returns:
        A GoogleResult object."""

    results = []

    html = get_html(word, num)

    if len(html) > 0:
        i = 1
        for page in html:

            soup = BeautifulSoup(page, "html.parser")

            result = soup.find("ol", attrs={"id": "b_results"})

            if not result:
                continue

            divs = result.find_all('li', attrs={"class":"b_algo"})

            if not result:
                continue

            recommand = _get_recommand(result.find('li', {'class': 'b_ans'}))

            results_div = soup.find("div", attrs={"id": "b_tween"}).find_all('span', {'class':'sb_count'})

            number_of_results = _get_number_of_results(results_div)

            attrs = result.find('li', attrs={"class": "b_pag"}).find_all('a')[i+2].attrs

            j = 0
            for li in divs:
                res = BingResult()

                res.page = i
                res.index = j

                res.name = _get_name(li)
                res.link = _get_link(li)
                print('get link', res.link)
                res.google_link = _get_google_link(li)
                res.description = _get_description(li)
                res.thumb = _get_thumb()
                res.cached = _get_cached(li)
                res.number_of_results = number_of_results
                res.recommand = recommand

                results.append(res)
                j += 1
            i += 1
    return results


def _get_recommand(recommand_div):
    if recommand_div == None:
        return None
    lis = recommand_div.find_all('a')
    a_list = []
    for a in lis:
        if a is not None:
            a_list.append(a.text.strip())
    if len(a_list) == 0:
        return None
    return a_list



# PRIVATE
def _get_name(li):
    """Return the name of a google search."""
    a = li.find("a")
    # return a.text.encode("utf-8").strip()
    if a is not None:
        return a.text.strip()
    return None


def _filter_link(link):
    '''Filter links found in the Google result pages HTML code.
    Returns None if the link doesn't yield a valid result.
    '''
    try:
        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        # link type-1
        # >>> "https://www.gitbook.com/book/ljalphabeta/python-"
        if o.netloc:
            return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return ''


def _get_link(li):
    """Return external link from a search."""
    try:
        a = li.find("a")
        link = a["href"]
    except Exception:
        return None
    return _filter_link(link)


def _get_google_link(li):
    """Return google link from a search."""
    try:
        a = li.find("a")
        link = a["href"]
    except Exception:
        return None

    if link.startswith("/url?") or link.startswith("/search?"):
        return urllib.parse.urljoin("http://www.google.com", link)

    else:
        return None


def _get_description(li):
    """Return the description of a google search.

    TODO: There are some text encoding problems to resolve."""

    sdiv = li.find("div", attrs={"class": "b_caption"})
    if sdiv:
        stspan = sdiv.find("p")
        if stspan is not None:
            # return stspan.text.encode("utf-8").strip()
            return stspan.text.strip()
    else:
        return None


def _get_thumb():
    """Return the link to a thumbnail of the website."""
    pass


def _get_cached(li):
    """Return a link to the cached version of the page."""
    links = li.find_all("a")
    if len(links) > 1 and links[1].text == "Cached":
        link = links[1]["href"]
        if link.startswith("/url?") or link.startswith("/search?"):
            return urllib.parse.urljoin("http://www.google.com", link)
    return None

def _get_number_of_results(results_div):
    """Return the total number of results of the google search.
    Note that the returned value will be the same for all the GoogleResult
    objects from a specific query."""
    try:
        results_div_text = results_div.get_text()
        if results_div_text:
            regex = r"((?:\d+[,\.])*\d+)"
            m = findall(regex, results_div_text)

            # Clean up the number.
            num = m[0].replace(",", "").replace(".", "")

            results = int(num)
            return results
    except Exception as e:
        return 0
