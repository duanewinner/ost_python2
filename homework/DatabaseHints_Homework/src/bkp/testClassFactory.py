#!/usr/local/bin/python3

import mysql.connector
import unittest

from database import login_info
from classFactory import build_row
from randstring import randstring

class DBTest(unittest.TestCase):
    
    def setUp(self):

        self.musician_tuple = (
            ("Chris Squire", "bass", "csquire@yes.com"),
            ("Bill Bruford", "drums", "bbruford@yes.com"),
            ("Steve Howe", "guitar", "showe@yes.com"),
            ("Geddy Lee", "bass", "glee@rush.com"),
            ("Neil Peart", "drums", "npeart@rush.com"),
            ("Alex Lifeson", "guitar", "alifeson@rush.com")
            )        

        self.db = mysql.connector.Connect(**login_info)
        self.cursor = self.db.cursor()
        self.tmp_musician_t=randstring()

        # Probably don't need this because unlikely to drop a tmp table
        self.cursor.execute("""DROP TABLE IF EXISTS %s""" % self.tmp_musician_t)
        # Create tmp animal table
        self.cursor.execute("""
            CREATE TABLE %s (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name varchar(50),
                instrument varchar(25),
                email VARCHAR(50))
            """ % self.tmp_musician_t)

        # Then populate
        for musician in self.musician_tuple:
            lrecord=("INSERT INTO %s " % self.tmp_musician_t) + \
                ("(name, instrument, email) VALUES ('%s', '%s', '%s')" % musician)
            self.cursor.execute(lrecord)
        self.db.commit()

#    def tearDown(self):
#        self.cursor.execute("""DROP TABLE %s""" % self.tmp_musician_t)


    def test_get(self):
        pass
#        observed = 
#        expected = 
#        self.assertEqual(observed, expected)



if __name__=="__main__":
    unittest.main(warnings='ignore')
#    unittest.main()
