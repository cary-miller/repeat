#!  /usr/bin/env python

import random
import time
import unittest
from catch import catch 


############################################################################
################################### Test ###################################
############################################################################


class FooBase(unittest.TestCase):

    def runTest(self): pass

    def setUp(self):
        self.ok = lambda r: r < 2
        self.try_hard = repeat_until_satisfied(self.ok, bad_outcome = bob)


class FooTest(FooBase):

    def test_catch(self):
        '''
        '''
        self.assertTrue( False )


    def test_good_outcome(self):
        func = self.try_hard(lambda:1)
        self.assertEqual(func(), 1)


ft = FooTest()

def test():
    unittest.main()


try:
    __file__
    if __name__ == '__main__':
        unittest.main()
except NameError:
    print 'interactive'

