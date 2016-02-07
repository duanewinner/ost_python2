#!/usr/bin/python3
"""
Read in and parse email messages to verify readability.

NOTE: This test creates teh message table, dropping any
previous version and should leave it empty. DANGER: this
test will delete any existing message table.
"""

from glob import glob
from email import message_from_string
import mysql.connector as msc
from database import login_info
import jotd
import os
import random
import tempfile
import unittest
import datetime
from email.utils import parsedate_tz, mktime_tz

conn = msc.Connect(**login_info)
curs = conn.cursor()

def randstring(length=16):
    """
    This is a random string generator.
    Will be used here to generate "fake" 
    jokes to populate the joke of the day table.
    """     
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))


TBLDEF = """\
CREATE TABLE jotd_emails (
     msgID INTEGER AUTO_INCREMENT PRIMARY KEY,
     msgMessageID VARCHAR(128),
     msgDate DATETIME,
     msgSenderName VARCHAR(128),
     msgSenderAddress VARCHAR(128),
     msgRecipientName VARCHAR(128),
     msgRecipientAddress VARCHAR(128),
     msgJotdName LONGTEXT,
     msgJotdText LONGTEXT
)"""

class testRealEmail_traffic(unittest.TestCase):
    def setUp(self):
        """
        Creates a temporary directory with 500 "dummy" jokes
        (randomly generated filenames each with 250 random chars).
        """
        self.workingdir = os.getcwd()
        self.jokesdir = tempfile.mkdtemp()
        os.chdir(self.jokesdir)
        for joke in range(500):
            jfile = randstring(8)
            f = open(jfile, 'w')
            f.write(randstring(250))
            f.close()

        """
        Creates a unique message in the jotd_emails table
        for each recipient for 500 days, using files in the 
        temporary jokes directory as dummy text content.

        WARNING: This will replace the content of any existing
        data in jotd_emails table. If this is undesirable, please 
        edit the database.py module to point to an alternative
        server and/or database for testing.
        """
        curs.execute("DROP TABLE IF EXISTS jotd_emails")
        conn.commit()
        curs.execute(TBLDEF)
        conn.commit()
        jotd.build_msgs("website@examle.com", "website@example.com", self.jokesdir)


    def test_full_count(self):
        """
        Because we tested with settings of 3 users and 500 days
        we should see a total of 1500 messages
        """
        self.assertEqual(jotd.msg_count(), 1500)

    def test_one_day_count(self):
        """
        Because we tested with settings of 3 users,
        we should see a total of 3 messages for just one day
        """
        self.assertEqual(jotd.msg_count(), 3)


if __name__ == "__main__":
    unittest.main()

