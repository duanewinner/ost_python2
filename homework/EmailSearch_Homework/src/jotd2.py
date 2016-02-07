#!/usr/bin/python3

import datetime
from email.utils import make_msgid 
from glob import glob
import mysql.connector
import os

from database import login_info
from settings import RECIPIENTS,STARTTIME,DAYCOUNT

db = mysql.connector.Connect(**login_info)
cursor = db.cursor()

table_name = "jotd_emails"

TBLDEF = """\
CREATE TABLE %s (
     msgID INTEGER AUTO_INCREMENT PRIMARY KEY,
     msgMessageID VARCHAR(128),
     msgDate DATETIME,
     msgSenderName VARCHAR(128),
     msgSenderEmail VARCHAR(128),
     msgRecipientName VARCHAR(128),
     msgRecipientEmail VARCHAR(128),
     msgJotdName LONGTEXT,
     msgJotdText LONGTEXT
)"""

def build_msgs(senderName, senderEmail, jokesDir):
    """
    Arguments to be supplied are: senderName, senderEmail, jokesDir, (Optional: tableName)
    Creates database table "jotd_emails" and populates the table with jokes in "jokesdir" directory.

    settings.py must exist in the same directory in the following format example:
    RECIPIENTS = [('John Doe', 'jdoe@abc.abc'), ('Alice Smith', 'asmith@abc.abc'), ('Charlie Brown', 'cbrown@abc.abc')]
    STARTTIME = "YYYY-MM-DD"
    DAYCOUNT = <integer>

    (Where):
    RECIPIENTS is a list of tuples: recipient name and recipient email.
    STARTTIME is a string in the format of 4-digit-year, 2-digit-month, and 2-digit-day
    DAYCOUNT is the integer of days to send your "Joke of the Day" while you are on vacation or leave-of-absence.

    WARNING: This is a destructive function. build_msgs will drop the existing table and rebuild.
    If undesirable, please consider supplying an alternative database.py with different server and/or database parameters.
    """

    cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
    db.commit()
    cursor.execute(TBLDEF % table_name)
    db.commit()

    jokes = [joke for joke in glob(os.path.join(jokesDir, '*'))]
    for day in range (DAYCOUNT):
        jotdName = os.path.basename(jokes[day])
        with open(jokes[day], 'r') as f:
            jotdText = f.read()
            f.closed
        msgDate = datetime.date.today() + datetime.timedelta(days=day)

        for recipientName,recipientEmail in RECIPIENTS:
            msgMessageID = make_msgid()
            query=("INSERT INTO %s " % table_name) + \
                    ("(msgMessageID, msgDate, msgSenderName, msgSenderEmail, msgRecipientName, \
                       msgRecipientEmail, msgJotdName, msgJotdText) VALUES \
                      ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                     (msgMessageID, msgDate, senderName, senderEmail, recipientName, recipientEmail, jotdName, jotdText) )
            cursor.execute(query)
            db.commit()

def msg_count(days=0):
    query = ("SELECT COUNT(*) FROM %s ;" % table_name)
    cursor.execute(query)
    return(cursor.fetchone()[0])


