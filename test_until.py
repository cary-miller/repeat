
import random
import time


def report(func, i, max_tries, response, *pos, **kw):
    print '   ', func.func_name, i, response
    return


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



