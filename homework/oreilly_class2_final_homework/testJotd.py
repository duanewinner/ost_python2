#!/usr/bin/python3
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

import datetime
import os
import random
import shutil
import tempfile
import unittest

import mysql.connector
from database import login_info

import jotd

def randstring(length=16):
    """
    This is a random string generator, handy for on-the-fly temporary
    db table creation when unittesting. Will also be used here to
    generate "fake" jokes to populate the joke of the day table.
    """     
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))


class testJOTD(unittest.TestCase):

    def setUp(self):
        """
        Create our test fixtures 
        """

        self.workingdir = os.getcwd()

        """
        Create a jokes directory and populate it with 500 
        dummy files with dummy text to simulate jokes.
        """
        self.jokesdir = tempfile.mkdtemp()
        os.chdir(self.jokesdir)
        for joke in range(500):
            jfile = randstring(8)
            f = open(jfile, 'w')
            f.write(randstring(250))
            f.close()

        """
        Create a tempory table for the messages for testing.
        Makes testing safe by using random temp name,
        and not production data/table.
        """
        MSGTBLDEF = """\
            msgID INTEGER AUTO_INCREMENT PRIMARY KEY,
            msgMessageID VARCHAR(128),
            msgDate DATETIME,
            msgSenderAddress VARCHAR(128),
            msgRecipientName VARCHAR(128),
            msgRecipientAddress VARCHAR(128),
            msgJotdName LONGTEXT,
            msgJotdText LONGTEXT
            """
        self.temp_jotd_emails_table=randstring()
        self.db = mysql.connector.Connect(**login_info)
        self.cursor = self.db.cursor()
        self.cursor.execute("""DROP TABLE IF EXISTS %s""" % self.temp_jotd_emails_table) # Probably not necessary
        self.db.commit()
        self.cursor.execute("""
            CREATE TABLE %s (
                %s)
                """ % (self.temp_jotd_emails_table, MSGTBLDEF))
        self.db.commit()

        """
        Testing assumes that the settings.py file contains the following:
           RECIPIENTS = [('John Doe', 'jdoe@abc.abc'), ('Alice Smith', 'asmith@abc.abc'), ('Charlie Brown', 'cbrown@abc.abc')]
           STARTTIME = "2015-03-20"
           DAYCOUNT = 500
        """

        """
        Populate the jotd table and messages
        """
        jotd.build_msgs("website@example.com", self.jokesdir, self.temp_jotd_emails_table)
        
    def tearDown(self):
        """
        Cleanup. Remove test fixtures; temp dir and temp db table.
        """
        os.chdir(self.workingdir)
        shutil.rmtree(self.jokesdir)
        #self.cursor.execute("""DROP TABLE %s""" % self.temp_jotd_emails_table)

    def test_oneday_msg_count(self):
        """
        Because we tested with settings of 3 users and 1 day
        we should see a total of 3 messages (one message per user for 1 day)
        """
        self.assertEqual(jotd.msg_count(self.temp_jotd_emails_table), 1500)




if __name__ == "__main__":
#    unittest.main(warnings='ignore')
    unittest.main()


