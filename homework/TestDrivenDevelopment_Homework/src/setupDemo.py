"""
Demonstration of setUp and tearDown.
The test do not actually test anything - this is a demo.
"""
import unittest
import tempfile
import shutil
import glob
import os

class FileTest(unittest.TestCase):
    
    def setUp(self):
        self.origdir = os.getcwd()
        self.dirname = tempfile.mkdtemp("testdir")
#        print("Created", self.dirname)
        os.chdir(self.dirname)
        
    def tearDown(self):
        os.chdir(self.origdir)
        shutil.rmtree(self.dirname)
#        print("Deleted", self.dirname)
        
    def test_1(self):
        "Verify creation of files is possible"
        myFilenames = {"this.txt", "that.txt", "the_other.txt"}
#        for filename in ("this.txt", "that.txt", "the_other.txt", "yours.txt"):
        for filename in myFilenames:
            f = open(filename, "w")
            f.write("Some text\n")
            f.close()
            self.assertTrue(f.closed)
        thoseFilenames = set(os.listdir())
        "Verify that each node is a file (i.e., not a directory"
        for node in thoseFilenames:
            self.assertTrue(os.path.isfile(node), node + " is not a file")
        """Verify that the files in the test directory reflect only
        the files supposed to be created.
        """
        self.assertEqual(myFilenames, thoseFilenames, \
                "Filenames in temp dir do not match what should exist.")
            
    def test_2(self):
        "Verify that the current directory is empty"
        self.assertEqual(glob.glob("*"), [], "directory is not empty")
    
    def test_3(self):
        "Verify creation of 1 million byte file"
        f = open("myFile", "wb")
        f.write(b'\x00' * 1000000)
        f.close()
        self.assertEqual((os.stat("myFile")).st_size, 1000000, "myFile is not 1 million bytes")

if __name__ == "__main__":
    unittest.main()
