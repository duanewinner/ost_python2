#!/usr/local/bin/python3

import mysql.connector
from database import login_info

db = mysql.connector.Connect(**login_info)
cursor = db.cursor()

# Verifies that every animal eats at least one food;
# returns first result of any animal that does not have a food.
def nofood(animal_t, food_t):
    lquery=("SELECT name,family FROM %s " % animal_t) + \
        ("where id not in (select anid from %s where feed is not NULL and feed !='')" % food_t)
    cursor.execute(lquery)
    result = cursor.fetchone()
    if result:
        return "%s the %s has no food." % result
    db.close()


