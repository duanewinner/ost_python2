#!/usr/local/bin/python3

import unittest
import tempfile
import shutil
import os
import curdir

class TestExtCount(unittest.TestCase):
    """Test case to verify file extension count function"""
    
    def setUp(self):
        self.file_names=["boxofrain.doc", "friendofdevil.doc", \
                         "sugarmagnolia.pdf", "operator"]
        self.origdir = os.getcwd()
        self.dirname = tempfile.mkdtemp("testdir")
        os.chdir(self.dirname)
        for fn in self.file_names:
            f = open(fn, "w")
            f.close()
        self.dirname = tempfile.mkdtemp("ripple")

    def tearDown(self):
        os.chdir(self.origdir)
        shutil.rmtree(self.dirname)
    
    def test_ext_count(self):
        observed = curdir.extcount()
        expected = "doc file count = 2\npdf file count = 1"
        self.assertEqual(observed, expected)

if __name__ == "__main__":
    unittest.main()
