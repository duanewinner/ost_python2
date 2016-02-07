#!/usr/local/bin/python3

"""
test what happens when a test fails
"""

import unittest, random

class TCase(unittest.TestCase):

    def setUp(self):
        print('\n\nsetUp here') #don't do this at home - test should never print
        #uncomment to randomly generate an error
        if random.randint(0,1): # produces either 0 or 1
            1/0   #produce an error if true

    def test_pass_1(self):
        print('test_pass_1')
        self.assertEqual(1,1)
    
    def test_pass_2(self):
        print('test_pass_2')
        self.assertEqual(1,1)
    
    def test_fail_1(self):
        print('test_fail_1')
        self.assertEqual(1,2)

    def test_fail_2(self):
        print('test_fail_2')
        self.assertEqual(1,2)

    def tearDown(self):
        print('tearDown here')
        
if __name__ == "__main__":
    ff=unittest.main()

