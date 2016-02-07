#!/usr/local/bin/python3

import unittest
import os
import random

import mysql.connector
from database import login_info
import foodval

# Return a random gen. all-char string -- useful for tmp db tables.
def randstring(length=16):
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))


class TestEatFoodVal(unittest.TestCase):
    """Test that eatfoodval correctly validates if an animal eats food"""

    def setUp(self):

        self.db = mysql.connector.Connect(**login_info)
        self.cursor = self.db.cursor()
 
        self.tmp_animal_t=randstring()
        self.tmp_food_t=randstring()

        self.animal_tuple = (
            ("Ellie", "Elephant", 2350),
            ("Gerald", "Gnu", 1400),
            ("Gerald", "Giraffe", 940),
            ("Leonard", "Leopard", 280),
            ("Sam", "Snake", 24),
            ("Steve", "Snake", 35),
            ("Zorro", "Zebra", 340),
            ("Hank", "Pet Rock", 5) 
            )

        self.food_list = [
            ('Ellie', 'Elephant', ['hay', 'peanuts']),
            ('Gerald', 'Gnu', ['leaves', 'shoots']),
            ('Gerald', 'Giraffe', ['hay', 'grass']),
            ('Leonard', 'Leopard', ['meat']),
            ('Sam', 'Snake', ['mice', 'meat']),
            ('Steve', 'Snake', ['mice', 'meat']),
            ('Zorro', 'Zebra', ['grass', 'leaves'])
            ]

        # Probably don't need this because unlikely to drop a tmp table
        self.cursor.execute("""DROP TABLE IF EXISTS %s""" % self.tmp_animal_t)
        # Create tmp animal table
        self.cursor.execute("""
            CREATE TABLE %s (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name varchar(50),
                family VARCHAR(50),
                weight INTEGER)
            """ % self.tmp_animal_t)

        # Then populate
        for animal in self.animal_tuple:
            lrecord=("INSERT INTO %s " % self.tmp_animal_t) + \
                ("(name, family, weight) VALUES ('%s', '%s', '%s')" % animal)
            self.cursor.execute(lrecord)
        self.db.commit()

        # Probably don't need this because unlikely to drop a tmp table
        self.cursor.execute("""DROP TABLE IF EXISTS %s""" % self.tmp_food_t)
        # Create tmp food table
        self.cursor.execute("""
            CREATE TABLE %s (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                anid INTEGER,
                feed VARCHAR(20),
                FOREIGN KEY (anid) REFERENCES animal(id))
            """ % self.tmp_food_t)

        # Then populate
        for name, family, foods in self.food_list:
            lquery=("SELECT id FROM %s " % self.tmp_animal_t) + \
                ("where name='%s' and family='%s'" % (name, family))
            self.cursor.execute(lquery)
            id = self.cursor.fetchone()[0]
            for food in foods:
                lrecord=("INSERT INTO %s " % self.tmp_food_t) + \
                    ("(anid, feed) VALUES ('%s', '%s')" % (id, food) )
                self.cursor.execute(lrecord)
        self.db.commit()
        
    def tearDown(self):
        self.cursor.execute("""DROP TABLE %s""" % self.tmp_animal_t)
        self.cursor.execute("""DROP TABLE %s""" % self.tmp_food_t)

    # Tests if animal with no food in food table is returned
    def test_eatfoodval(self):
        observed = foodval.nofood(self.tmp_animal_t,self.tmp_food_t)
        expected = "Hank the Pet Rock has no food."
        self.assertEqual(observed, expected)

    # Does the same thing as above, but tests if animal is in food table
    # but feed is set to NULL
    def test_eatfoodval_when_NULL(self):

        lquery=("SELECT id FROM %s " % self.tmp_animal_t) + \
            ("where name='%s' and family='%s'" % ("Hank", "Pet Rock"))
        self.cursor.execute(lquery)
        id = self.cursor.fetchone()[0]
        lrecord=("INSERT INTO %s " % self.tmp_food_t) + \
            ("(anid, feed) VALUES ('%s', NULL)" % (id) )
        self.cursor.execute(lrecord)
        self.db.commit()

        observed = foodval.nofood(self.tmp_animal_t,self.tmp_food_t)
        expected = "Hank the Pet Rock has no food."
        self.assertEqual(observed, expected)

    # Finally, test for no food; tests if animal is in food table
    # but feed is set to an empty string (not NULL).
    def test_eatfoodval_when_empty_string(self):

        lquery=("SELECT id FROM %s " % self.tmp_animal_t) + \
            ("where name='%s' and family='%s'" % ("Hank", "Pet Rock"))
        self.cursor.execute(lquery)
        id = self.cursor.fetchone()[0]
        lrecord=("INSERT INTO %s " % self.tmp_food_t) + \
            ("(anid, feed) VALUES ('%s', '')" % (id) )
        self.cursor.execute(lrecord)
        self.db.commit()

        observed = foodval.nofood(self.tmp_animal_t,self.tmp_food_t)
        expected = "Hank the Pet Rock has no food."
        self.assertEqual(observed, expected)

    # Last but not least, ensure that the food validator still works
    # if an animal has food.
    def test_eatfoodval_when_has_food(self):

        lquery=("SELECT id FROM %s " % self.tmp_animal_t) + \
            ("where name='%s' and family='%s'" % ("Hank", "Pet Rock"))
        self.cursor.execute(lquery)
        id = self.cursor.fetchone()[0]
        lrecord=("INSERT INTO %s " % self.tmp_food_t) + \
            ("(anid, feed) VALUES ('%s', 'Air')" % (id) )
        self.cursor.execute(lrecord)
        self.db.commit()

        observed = foodval.nofood(self.tmp_animal_t,self.tmp_food_t)
        expected = None
        self.assertEqual(observed, expected)

    
if __name__ == "__main__":
    unittest.main(warnings='ignore')
#    unittest.main()
