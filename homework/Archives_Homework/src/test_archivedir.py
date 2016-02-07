#!/usr/local/bin/python3

"""
Here are your instructions:

The zipfile example in the lesson text stores the full path of the files that
it saves to the zipfile. Normally, however, zipfiles contain only a relative
pathname (you will see that when the names are listed after the zipfile is
created, the "v:\\" has been removed).

Create a project named Archives_Homework and add it to the Python2_Homework
working set. In this project, write a function that takes a directory path
and creates an archive of the directory only. For example, if the same path 
were used as in the example ("v:\\workspace\\Archives\\src\\archive_me"), the
zipfile would contain "archive_me\\groucho" "archive_me\\harpo" and
"archive_me\\chico." Note that zipfile.namelist() always uses forward slashes
in what it returns, a fact you will need to accommodate when comparing observed
and expected.

The base directory ("archive_me" in the example above) is the final element of
the input, and all paths recorded in the zipfile should start with the base
directory.

If the directory contains subdirectories, the subdirectory names and any files
in the subdirectories should not be included. (Hint: You can use isfile() to determine if a filename represents a regular file and not a directory.)
"""
 
import os
import shutil
import tempfile
import unittest
import zipfile

import archivedir

class TestZipDir(unittest.TestCase):
    """Test case to verify zipfile creation from directory function"""

    def setUp(self):
        self.working_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        self.zip_filename = os.path.join(os.path.dirname(self.test_dir),
                                         os.path.basename(self.test_dir)
                                         + ".zip")
        self.file_names=["abc.doc", "def.doc", "ghi.doc"]
        os.chdir(self.test_dir)
        for fn in self.file_names:
            f = open(fn, "w")
            f.close()
        # Create bogus directory in tmpdir to make sure function omits this:
        os.mkdir(os.path.join(self.test_dir, "jkl"))

    def tearDown(self):
        os.chdir(self.working_dir)
        shutil.rmtree(self.test_dir)
        os.remove(self.zip_filename)

    def testZipDir(self):
        archivedir.zipdir_depth1(self.test_dir, self.zip_filename)
        zip_object = zipfile.ZipFile(self.zip_filename, "r")
        files_in_zipfile = zip_object.namelist()
        zip_object.close()
        observed = set([os.path.basename(item) for item in files_in_zipfile])
        expected = set(self.file_names)
        self.assertEqual(observed, expected)

if __name__ == "__main__":
    unittest.main()
