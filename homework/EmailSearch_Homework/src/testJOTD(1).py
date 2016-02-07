#!/usr/local/bin/python3
"""
Python 2: Getting More Out of Python  Lesson 13, Project 1

Here are your instructions:

Write a program that imports the following names from a "settings" module:
RECIPIENTS   a list of (name, email-address) tuples
STARTTIME    datetime.datetime object for first message
DAYCOUNT    number of daily message generations

The program should produce a message of the format:
Date: {{date}}
From: <a href="mailto:website@example.com">website@example.com</a>
To: {{recipient}}
Message-Id: <NNNNNN>

This is a test message.

Your program should save these messages in the messages table.

Use test-driven development, and state the purpose of each test in the suite in docstrings that will eventually document your program.

Time your program for DAYCOUNTS of 1, 10, 50, 100, and 500 and plot the results (on a sheet of paper). How reliable are the timings?

Think of it like this: You are soon to go on vacation, at STARTTIME, for DAYCOUNT days, and you want your co-workers (RECIPIENTS) to continue getting your famous Joke of the Day (JOTD).

Your strategy is to store up the emails ahead of time, predated with the date they're to be sent. So if you leave on vacation on Jan 3, 2013, the first set of emails might be dated Jan 4 (each recipient gets one), then Jan 5 and so on, for DAYCOUNT days.

A good test that you have the right number is DAYCOUNT * len(RECIPIENTS) should equal SELECT COUNT(*) FROM jotd_emails; that is, the total number of days you're on vacation times the number of receivers, should equal the total number of records in the table generated. Of course, this will only be true if your To: line is only to a single recipient, and not all of them separated by commas.

Storing the right date for each email will likely involve using a timedelta to increment a datetime by one day at a time for DAYCOUNT days.

Regarding timing, it's enough to count under your breath and give a sense in your remarks about how you think time might be a function of DAYCOUNT. If you have your email generating and storing function where you might conveniently go:
    start = time.time()
    call_function(args)
    end = time.time()
    interval = end - start
    print("Time to complete: ", end)

Then you could also give some hard numbers as to the relative times the program took as a function of changing DAYCOUNT. The purpose of this requirement is to look ahead to future projects where timing / profiling is a core focus.
"""

import os
import random
import shutil
import tempfile
import unittest

import mysql.connector
from database import login_info

def randstring(length=16):
    """
    This is a random string generator, handy for on-the-fly temporary
    db table creation when unittesting. Will also be used to generate "fake"
    jokes to populate the joke of the day table.
    """     
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))

def create_settings(recipients, starttime, daycount):
    """
    Since we want to try tests with different settings (# of recipents, date, days)
    We need to create different iterations of the settings.py module to test against.
    This function will take a string variable with these settings to create
    a "settings.py" module in a tempdir, on-the-fly by setUp.
    """
    f = open("settings.py", 'w')
    f.write("RECIPIENTS = " + str(recipients) + \
                "\nSTARTTIME = " + starttime + \
                "\nDAYCOUNT = " + str(daycount) + "\n")
    f.close()

JOKETBLDEF = """\
     jokeID INTEGER AUTO_INCREMENT PRIMARY KEY,
     jokeText LONGTEXT
    """
MSGTBLDEF = """\
     msgID INTEGER AUTO_INCREMENT PRIMARY KEY,
     msgMessageID VARCHAR(128),
     msgDate DATETIME,
     msgSenderName VARCHAR(128),
     msgSenderAddress VARCHAR(128),
     msgText LONGTEXT,
     msgJokeID,
     FOREIGN KEY (msgJokeID) REFERENCES jotd_joke(jokeID)
    """


class testJOTD(unittest.TestCase):
    def setUp(self):
        """
        Create a temp directory so we can write out the different
        values for setting.py module, using create_settings function,
        based on the variables of each test case.
        """
        self.tmpdir = tempfile.mkdtemp()
        self.workingdir = os.getcwd()
        os.chdir(self.tmpdir)

        """
        Setup database connection and
        create temporary database tables for testing.  
        """
        self.db = mysql.connector.Connect(**login_info)
        self.cursor = self.db.cursor()

        # Generate random strings for table names
        self.tmp_jotd_t=randstring()
        self.tmp_message_t=randstring()

        # Probably don't need this because unlikely to drop a tmp table
        self.cursor.execute("""DROP TABLE IF EXISTS %s""" % self.tmp_jotd_t)
        # Create tmp jotd table
        self.cursor.execute("""
            CREATE TABLE %s (
                %s)
            """ % (self.tmp_jotd_t, JOKETBLDEF))
        """
        We trust that Mr. Funny Man has his own method of populating a stash of jokes.
        We don't have a deep well of humor, so we'll just simulate pre-existing 500 jokes
        with some random nonsense.
        """
        for joke in range(500):
            lrecord=("INSERT INTO %s " % self.tmp_jotd_t) + \
                ("(jokeText) VALUES ('%s')" % randstring(250))
            self.cursor.execute(lrecord)
        self.db.commit()

    def tearDown(self):
        """
        Cleanup. Remove tmpdir holding settings.py
        and drop db tables.
        """
        os.chdir(self.workingdir)
        shutil.rmtree(self.tmpdir)

    def test1(self):
        # 1 recipient, one day
        recipients = [("John Doe", "jdoe@abc.abc")]
        starttime = "2015-03-30"
        daycount = 1
        create_settings(recipients, starttime, daycount)

"""
    def test2(self):
        # 1 recipient, 5 days
        recipients = [("John Doe", "jdoe@abc.abc")]
        starttime = "2015-06-17"
        daycount = 5
        create_settings(recipients, starttime, daycount)

    def test3(self):
        # 2 recipients, 5 days
        recipients = [('John Doe', 'jdoe@abc.abc'), ('Alice Smith', 'asmith@abc.abc')]
        starttime = "2015-06-17"
        daycount = 5
        create_settings(recipients, starttime, daycount)

    def test4(self):
        # 2 recipients, 10 days
        recipients = [('John Doe', 'jdoe@abc.abc'), ('Alice Smith', 'asmith@abc.abc')]
        starttime = "2015-06-17"
        daycount = 10
        create_settings(recipients, starttime, daycount)

    def test5(self):
        # 2 recipients, 50 days
        recipients = [('John Doe', 'jdoe@abc.abc'), ('Alice Smith', 'asmith@abc.abc')]
        starttime = "2015-06-17"
        daycount = 10
        create_settings(recipients, starttime, daycount)
"""

if __name__ == "__main__":
    unittest.main(warnings='ignore')
#    unittest.main()

