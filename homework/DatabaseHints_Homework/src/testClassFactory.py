#!/usr/local/bin/python3

import unittest
import os
import random
from pprint import pprint

import mysql.connector
from database import login_info
from classFactory import build_row

# Return a random gen. all-char string -- useful for tmp db tables. 
def randstring(length=16):
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))

class DBTest(unittest.TestCase):
    
    def setUp(self):

        self.db = mysql.connector.Connect(**login_info)
        self.cursor = self.db.cursor()
 
        self.tmp_poc_t=randstring()

        self.poc_seed = (
            ("jdoe", "John", "Doe", "jdoe@myairline.com"),
            ("dpeters", "David", "Peters", "dpeters@myairline.com"),
            ("asmith", "Alice", "Smith", "asmith@myairline.com"),
            ("brogers", "Bob", "Rogers", "bob.rogers@xyzfly.com"),
            ("tlittle", "Tom", "Little", "tom.little@xyzfly.com"),
            ("mwallace", "Moe", "Wallace", "moe.wallace@xyzfly.com")
            )

        # Probably don't need this because unlikely to drop a tmp table. 
        self.cursor.execute("DROP TABLE IF EXISTS %s" % self.tmp_poc_t)
        # Create tmp poc table
        self.cursor.execute("""
            CREATE TABLE %s (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username varchar(50),
                firstname VARCHAR(50),
                lastname VARCHAR(50),
                email VARCHAR(50))
            """ % self.tmp_poc_t)

        # Then populate
        for poc in self.poc_seed:
            lrecord=("INSERT INTO %s " % self.tmp_poc_t) + \
                ("(username, firstname, lastname, email) VALUES ('%s', '%s', '%s', '%s')" % poc)
            self.cursor.execute(lrecord)
        self.db.commit()

        # Create DataRow object an instantiate a blank instance of DataRow object
        self.POC=build_row(self.tmp_poc_t, "id username firstname lastname email")
        self.poc=self.POC([None,None,None,None,None])

    def tearDown(self):
        self.cursor.execute("DROP TABLE %s" % self.tmp_poc_t)
        
    def test_retrieve(self):
        names=[]
        rows=self.poc.retrieve(self.cursor, "where email like \"%myairline.com\"")
        for row in rows:
            names.append(str(row.firstname)+" "+str(row.lastname))
        self.assertEqual(names, ["John Doe", "David Peters", "Alice Smith"])


if __name__ == "__main__":
    unittest.main(warnings='ignore')


