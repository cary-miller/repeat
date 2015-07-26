import random
import functools

def typical_func(tries=0):
    res = 'error'
    if tries < 4:
        res = random.choice(range(11))
        if res != 0:
            return typical_func(tries+1)
    return res


def better_recursive(tries=0):
    if tries >= 4:
        return 'error'
    res = random.choice(range(11))
    if res == 0:
        return res
    return typical_func(tries+1)


def br2(tries=0):
    if tries >= 4:
        return 'error'
    res = random.choice(range(11))
    return res if res == 0 else typical_func(tries+1)


def maybe_better():
    tries=0
    while tries < 4:
        tries += 1
        res = random.choice(range(11))
        if res == 0:
            return res
    return 'error'


def repeat_until_return_value_in(good_results, max_tries=5):
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            i = 0
            while i < max_tries:
                i += 1
                res = func(*pos, **kw)
                if res in good_results:
                    return res
            return 'error'
        return inner
    return outer


@repeat_until_return_value_in((0,))
def better():
    return random.choice(range(11))


@repeat_until_return_value_in((0, 7, 9), max_tries=3)
def also_better():
    return random.choice(range(11))


@repeat_until_return_value_in((2, 22,), max_tries=7)
def another_better():
    return random.choice(range(11))


def repeat_until_status_code_in(good_codes, max_tries=5): 
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            i = 0
            while i < max_tries:
                i += 1
                response = func(*pos, **kw)
                if response.status_code in good_codes:
                    return response
            return 'no good response in %s attempts' % max_tries
        return inner
    return outer


class NS(object):
    codes = [100, 200, 201, 300, 400, 404, 500]
    dct = dict(foo=2, boo='moo')
    for name in dct:
        name = dct[name]
ns = NS()

class MockResponse(object):
    codes = [100, 200, 201, 300, 400, 404, 500]
    def __init__(self, url, **kw):
        self.status_code = random.choice(self.codes)
        self.text = 'mock web service response. %s' % time.ctime()


def make_request(url):
    return MockResponse(url)


@repeat_until_status_code_in([200, 201], max_tries=7)
def yet_another(url):
    return make_request(url)


@repeat_until_status_code_in([200], max_tries=2)
def and_one_more(url):
    return make_request(url)


