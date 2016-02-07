#!/usr/bin/python3

import datetime
from email.utils import make_msgid 
import email
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

class Message:
    def __init__(self, msgMessageID, msgDate, msgSenderName, msgSenderEmail, msgRecipientEmail, msgJotdText):
        self.Date = msgDate
        self.From = "<a href=\"mailto:%s\">website@%s</a>" % (msgSenderName, msgSenderEmail)
        self.To = msgRecipientEmail
        self.MessageID = msgMessageID
        self.Text = msgJotdText

    def __repr__(self):
        return "Message('{0}', '{1}', '{2}', '{3}', '{4}')".format(
                self.Date, self.From, self.To, self.MessageID, self.Text)

    def message(self):
        msg =  email.message_from_string(self.Text)
        msg['Date'] = str(self.Date)
        msg['From'] = self.From
        msg['To'] = self.To
        msg['Message-ID'] = self.MessageID
        return(msg)


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
        fmtDate = datetime.datetime.strptime(STARTTIME, "%Y-%m-%d")
        msgDate = fmtDate + datetime.timedelta(days=day)

        for recipientName,recipientEmail in RECIPIENTS:
            msgMessageID = make_msgid()
            query=("INSERT INTO %s " % table_name) + \
                    ("(msgMessageID, msgDate, msgSenderName, msgSenderEmail, msgRecipientName, \
                       msgRecipientEmail, msgJotdName, msgJotdText) VALUES \
                      ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                     (msgMessageID, msgDate, senderName, senderEmail, recipientName, recipientEmail, jotdName, jotdText) )
            cursor.execute(query)
            db.commit()

def msg_count(days=None):
    """
    Returns the number of messages (total) which should be sent from
    the start date for X number of days.
    If no days are supplied, then will return total # of messages
    for the entire run.
    """
    COND = ""
    if days:
        query = ("SELECT COUNT(DISTINCT(msgDate)) FROM %s;" % (table_name))
        cursor.execute(query)
        days_in_table = cursor.fetchone()[0]
        if days_in_table < days:
            return("Days requested exceeds days in table (%s)" % (days_in_table))
        query = "SELECT MIN(msgDate) FROM %s;" % (table_name)
        cursor.execute(query)
        earliest_date = cursor.fetchone()[0]
        COND = "WHERE msgDate < '" \
               + str(datetime.datetime.strptime(str(earliest_date), "%Y-%m-%d %H:%M:%S") \
               + datetime.timedelta(days=days)) + "'"
    query = ("SELECT COUNT(*) FROM %s %s;" % (table_name, COND))
    cursor.execute(query)
    return(cursor.fetchone()[0])


def get_todays_messages(date=datetime.date.today()):
    """
    Returns a list of message objects to be sent today.
    """
    query = "SELECT msgMessageID, msgDate, \
                    msgSenderName, msgSenderEmail, \
                    msgRecipientEmail, msgJotdText \
                    FROM %s WHERE msgDate = '%s';" \
            % (table_name, date)
    cursor.execute(query)
    messages = [Message(*row) for row in cursor.fetchall()]
    message_list = []
    for message in messages:
        message_list.append(message.message())
    return(message_list)

