#!  /usr/bin/env python
#############!  ../../project/ve1/bin/python2.7
print 'yoohoo'
import random
import time
import unittest
#import mock
#from until import repeat
#repeat_until_satisfied = repeat.until.satisfied
from until import repeat_until_satisfied 


class MockResponse(object):
    codes = [100, 200, 201, 300, 400, 404, 500]
    def __init__(self, url, **kw):
        self.status_code = random.choice(self.codes)
        self.text = 'mock web service response. %s' % time.ctime()


def make_request(url):
    return MockResponse(url)


def report(func, i, max_tries, response, *pos, **kw):
    print '   ', func.func_name, i, response
    return


end_of_loop = lambda *a, **k: time.sleep(0.01)
#sc1 = lambda r: r.status_code in [200]
#sc2 = lambda r: r.status_code in [200, 201]
#lt2 = lambda r: r < 2
eq5 = lambda r: r == 5
boa = lambda m, r: ('bo', r, m)
bo_returns_tuple = lambda m, r: ('bo', r, m)
bob = lambda m, r: 'not satisfied'
bo_returns_string = lambda m, r: 'not satisfied'
#ry_harder = repeat_until_satisfied(lt2, max_tries=3, bad_outcome = boa)
generic = lambda: random.choice(range(11))
one = lambda:1
always_1 = lambda:1
always_returns_1 = lambda:1


#@repeat_until_satisfied(sc1, max_tries=2)
#def generala(url):
#    return make_request(url)
#
#
#@repeat_until_satisfied(sc2, max_tries=4)
#def generalb(url):
#    return make_request(url)
#
#
#@repeat_until_satisfied(lt2, max_tries=3)
#def generalc():
#    return generic()
#
#
#@repeat_until_satisfied(lt2, max_tries=3, bad_outcome = bob)
#def generald():
#    return generic()
#
#
#@try_harder
#def generale():
#    return generic()
#


############################################################################
################################### Test ###################################
############################################################################

# end_of_loop(i, max_tries, result, *pos, **kw)
eola = lambda *a, **k: None  
def eolb(i, max_tries, result, *pos, **kw):
    msg = '%s/%s %s %s %s' %(i, max_tries, result, str(pos), str(kw))
    print msg
eolc = lambda *a, **k: time.sleep(0.1)
return_value_is_5 = lambda r: r==5


def test_report(reportfunc):
    '''Repeat until function returns 5.
    '''
    return repeat_until_satisfied(return_value_is_5, report = reportfunc)


def test_end_of_loop(eolfunc):
    '''Repeat until function returns 5.
    '''
    return repeat_until_satisfied(return_value_is_5, end_of_loop = eolfunc)


def test_bad_outcome(bofunc): pass
def test_bad_outcome(bofunc): pass


def want_return_eq_5(bofunc):
    '''Repeat until function returns 5.
    '''
    return repeat_until_satisfied(return_value_is_5, bad_outcome = bofunc)



class FooBase(unittest.TestCase):

    def runTest(self): pass

    def setUp(self):
        self.ok = lambda r: r < 2
        self.try_hard = repeat_until_satisfied(self.ok, bad_outcome = bob)


class FooTest(FooBase):

    def test_bad_outcome(self):
        # Verify we get the correct return value when the funtion is
        # not satisfied (non-satisfiable in this case).
        value = want_return_eq_5(bo_returns_string)(always_returns_1)()
        self.assertEqual(value, 'not satisfied')
        value = want_return_eq_5(bo_returns_tuple)(always_returns_1)()
        self.assertEqual(value, ('bo', 1, 5))


    def end_of_loop_or_report(self, test_func):
        '''End-of-loop or report functionality.   Does the right thing happen?
        The complex case is failure every time,  so that is what gets tested.
        '''
        t0 = time.time()
        oc = test_func(eola)(one)()
        t1 = time.time() - t0
        self.assertTrue(oc.startswith('no good'))
        print 'a', t1
        self.assertTrue( t1 < 10**-3)

        # This block not much important.   Could check to be sure it prints
        # correctly.
        t0 = time.time()
        oc = test_func(eolb)(one)()
        tb = time.time() - t0
        self.assertTrue(oc.startswith('no good'))
        print 'b', tb
        self.assertTrue( tb > t1 )

        # This block is the most important in this test.   The timing shows that
        # the eolc func is executed each time through the loop.
        t0 = time.time()
        oc = test_func(eolc)(one)()
        tc = time.time() - t0
        self.assertTrue(oc.startswith('no good'))
        print 'c', tc
        self.assertTrue( tc > 0.5 )


    def test_end_of_loop(self):
        # Does the end_of_loop functionality behave properly?
        self.end_of_loop_or_report(test_end_of_loop)


    def test_report(self):
        # Does the report functionality behave properly?
        self.end_of_loop_or_report(test_report)


    def test_report_under_success(self):
        '''works same under both success and failure.   Failure already tested,
        no need to check success behavior.
        '''
        self.assertTrue( False )


    def test_good_outcome(self):
        func = self.try_hard(lambda:1)
        self.assertEqual(func(), 1)


    def test_max_tries(self):
        # how to do so?
        # probably have to watch for printed messages.
        self.assertTrue( False )




ft = FooTest()

def test():
    unittest.main()



try:
    __file__
    if __name__ == '__main__':
        unittest.main()
except NameError:
    print 'interactive'


