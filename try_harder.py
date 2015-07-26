import random
import functools
import time


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


def report(func, i, max_tries, response, *pos, **kw):
    print '   ', func.func_name, i, response
    return


def repeat_until_satisfied(ok, max_tries=5, 
        bad_outcome = lambda r, mt, *a, **k: 'no good result: %s attempts' % mt,
        report = lambda *a, **k: None,
        end_of_loop = lambda *a, **k: None,
    ): 
    '''
    ok:  a predicate,  returns truthiness.
    bad_outcome: a function
    report: a function
    end_of_loop: a function
    '''
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            i = 0
            while i < max_tries:
                i += 1
                result = func(*pos, **kw)
                report(func, i, max_tries, result, *pos, **kw)
                if ok(result):
                    return result
                end_of_loop(i, max_tries, result, *pos, **kw)
            return bad_outcome(result, max_tries, *pos, **kw)
        return inner
    return outer


end_of_loop = lambda *a, **k: time.sleep(0.01)
sc1 = lambda r: r.status_code in [200]
sc2 = lambda r: r.status_code in [200, 201]
lt2 = lambda r: r < 2
boa = lambda r, m: ('bo', r, m)
bob = lambda r, m: 'not satisfied'
try_harder = repeat_until_satisfied(lt2, max_tries=3, bad_outcome = boa)
generic = lambda: random.choice(range(11))


@repeat_until_satisfied(sc1, max_tries=2)
def generala(url):
    return make_request(url)


@repeat_until_satisfied(sc2, max_tries=4)
def generalb(url):
    return make_request(url)


@repeat_until_satisfied(lt2, max_tries=3)
def generalc():
    return generic()


@repeat_until_satisfied(lt2, max_tries=3, bad_outcome = bob)
def generald():
    return generic()


@try_harder
def generale():
    return generic()


############################################################################
################################### Test ###################################
############################################################################


import unittest
import mock

class FooBase(unittest.TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.ok = lambda r: r < 2
        self.ns = lambda r, m: 'not satisfied'
        self.try_hard = repeat_until_satisfied(self.ok, bad_outcome = self.ns)


class FooTest(FooBase):

    def test_bad_outcome(self):
        @self.try_hard
        def func():   # not satisfiable
            return 3
        self.assertEqual(func(), 'not satisfied')


    def test_good_outcome(self):
        func = self.try_hard(lambda:1)
        self.assertEqual(func(), 1)


ft = FooTest()

def test():
    unittest.main()


'''
martin fowler
What did we do well?
What have we learned?
What can we do better?
What puzzles us?
http://martinfowler.com/articles/richardsonMaturityModel.html
'''


def catch(Exc, action=lambda E,e: (E, e), reraise=True, *a, **k): 
    '''
    '''
    def outer(func):
        @functools.wraps(func)
        def inner(*pos, **kw):
            try:
                return func(*pos, **kw)
            except Exc, exc:
                action(Exc, exc)
                if reraise:
                    raise
        return inner
    return outer


class FooE(Exception): pass


def fx():
    if random.random() < 0.05:
        raise FooE('fooey')
    return random.choice(range(11))


def f1():
    return fx()


def logit(E, e):
    print E, e


@catch(FooE, logit)
def f2():
    return fx()


@repeat_until_satisfied(lambda r: r<2, max_tries=3, report=report)
@catch(FooE, logit, False)
def f3():
    return fx()


@catch(FooE, logit, False)
@repeat_until_satisfied(lambda r: r<2, max_tries=3)
def f4():
    return fx()



