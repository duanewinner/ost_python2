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

def build_msgs(sender, jokesdir, dbtable="jotd_emails"):
    """
    Populates the message table, using the jokes files in jokesdir
    and settings.py file to build each message.
    The directory of the jokes files must be supplied.
    Will use "jotd_emails" db table unless an alternative is supplied (ie., for testing)
    """
    jokes = [joke for joke in glob(os.path.join(jokesdir, '*'))]
    for day in range (DAYCOUNT):
        jotd_name = os.path.basename(jokes[day])
        with open(jokes[day], 'r') as f:
            jotd_text = f.read()
            f.closed
        msg_date = datetime.date.today() + datetime.timedelta(days=day)

        for r_name,r_email in RECIPIENTS:
            msg_id = make_msgid()
            query=("INSERT INTO %s " % dbtable) + \
                    ("(msgMessageID, msgDate, msgSenderAddress, msgRecipientName, \
                       msgRecipientAddress, msgJotdName, msgJotdText) VALUES \
                      ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                     (msg_id, msg_date, sender, r_name, r_email, jotd_name, jotd_text) )
            cursor.execute(query)
            db.commit()

def msg_count(dbtable="jotd_emails"):
    query = ("SELECT COUNT(*) FROM %s ;" % dbtable)
    cursor.execute(query)
    return(cursor.fetchone()[0])


