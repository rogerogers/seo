from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from future import standard_library
standard_library.install_aliases()
from builtins import range
from past.utils import old_div
import time
from selenium import webdriver
import urllib.request
import urllib.error
import urllib.parse
from functools import wraps
# import requests
from urllib.parse import urlencode
from fake_useragent import UserAgent
import sys

class AreaError(KeyError):
    pass


def measure_time(fn):

    def decorator(*args, **kwargs):
        start = time.time()

        res = fn(*args, **kwargs)

        elapsed = time.time() - start
        print(fn.__name__, "took", elapsed, "seconds")

        return res

    return decorator


def normalize_query(query):
    return query.strip().replace(":", "%3A").replace("+", "%2B").replace("&", "%26").replace(" ", "+")


def _get_search_url(query, page=0, per_page=10, lang='en', area='com', ncr=False, time_period=False, sort_by_date=False):
    # note: num per page might not be supported by google anymore (because of
    # google instant)

    params = {
        'nl': lang,
        'q': query.encode('utf8'),
        'start': page * per_page,
        'num': per_page
    }

    time_mapping = {
        'hour': 'qdr:h',
        'week': 'qdr:w',
        'month': 'qdr:m',
        'year': 'qdr:y'
    }


    tbs_param = []
    # Set time period for query if given
    if time_period and time_period in time_mapping:
        tbs_param.append(time_mapping[time_period])

    if sort_by_date:
        tbs_param.append('sbd:1')
    params['tbs'] = ','.join(tbs_param)

    # This will allow to search Google with No Country Redirect
    if ncr:
        params['gl'] = 'us' # Geographic Location: US
        params['pws'] = '0' # 'pws' = '0' disables personalised search
        params['gws_rd'] = 'cr' # Google Web Server ReDirect: CountRy.

    params['PC'] = 'U316'
    params['FROM'] = 'CHROMN'

    params = urlencode(params)

    url = 'https://www.bing.com/search?' + params


    # @author JuaniFilardo:
    # Workaround to switch between http and https, since this maneuver
    # seems to avoid the 503 error when performing a lot of queries.
    # Weird, but it works.
    # You may also wanna wait some time between queries, say, randint(50,65)
    # between each query, and randint(180,240) every 100 queries, which is
    # what I found useful.
    https = int(time.time()) % 2 == 0
    bare_url = u"https://www.bing.com/search?" if https else u"http://www.bing.com/search?"
    url = bare_url + params

    # return u"http://www.google.com/search?hl=%s&q=%s&start=%i&num=%i" %
    # (lang, normalize_query(query), page * per_page, per_page)
    url += params
    return url


def get_html(url):
    ua = UserAgent()
    header = ua.random

    try:
        request = urllib.request.Request(url)
        request.add_header("User-Agent", header)
        html = urllib.request.urlopen(request).read()
        return html
    except urllib.error.HTTPError as e:
        print("Error accessing:", url)
        print(e)
        if e.code == 503 and 'CaptchaRedirect' in e.read():
            print("Google is requiring a Captcha. "
                  "For more information check: 'https://support.google.com/websearch/answer/86640'")
        if e.code == 503:
            sys.exit("503 Error: service is currently unavailable. Program will exit.")
        return None
    except Exception as e:
        print("Error accessing:", url)
        print(e)
        return None


def write_html_to_file(html, filename):
    of = open(filename, "w")
    of.write(html.encode("utf-8"))
    # of.flush()
    of.close()


def get_browser_with_url(url, timeout=120, driver="firefox"):
    """Returns an open browser with a given url."""

    # choose a browser
    if driver == "firefox":
        browser = webdriver.Firefox()
    elif driver == "ie":
        browser = webdriver.Ie()
    elif driver == "chrome":
        browser = webdriver.Chrome()
    else:
        print("Driver choosen is not recognized")

    # set maximum load time
    browser.set_page_load_timeout(timeout)

    # open a browser with given url
    browser.get(url)

    time.sleep(0.5)

    return browser


def get_html_from_dynamic_site(url, timeout=120,
                               driver="firefox", attempts=10):
    """Returns html from a dynamic site, opening it in a browser."""

    RV = ""

    # try several attempts
    for i in range(attempts):
        try:
            # load browser
            browser = get_browser_with_url(url, timeout, driver)

            # get html
            time.sleep(2)
            content = browser.page_source

            # try again if there is no content
            if not content:
                browser.quit()
                raise Exception("No content!")

            # if there is content gets out
            browser.quit()
            RV = content
            break

        except:
            print("\nTry ", i, " of ", attempts, "\n")
            time.sleep(5)

    return RV


def timeit(func=None, loops=1, verbose=False):
    if func:
        def inner(*args, **kwargs):

            sums = 0.0
            mins = 1.7976931348623157e+308
            maxs = 0.0
            print('====%s Timing====' % func.__name__)
            for i in range(0, loops):
                t0 = time.time()
                result = func(*args, **kwargs)
                dt = time.time() - t0
                mins = dt if dt < mins else mins
                maxs = dt if dt > maxs else maxs
                sums += dt
                if verbose:
                    print('\t%r ran in %2.9f sec on run %s' %
                          (func.__name__, dt, i))
            print('%r min run time was %2.9f sec' % (func.__name__, mins))
            print('%r max run time was %2.9f sec' % (func.__name__, maxs))
            print('%r avg run time was %2.9f sec in %s runs' %
                  (func.__name__, old_div(sums, loops), loops))
            print('==== end ====')
            return result

        return inner
    else:
        def partial_inner(func):
            return timeit(func, loops, verbose)
        return partial_inner


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (f.__name__, args, kw, te - ts))
        return result
    return wrap
