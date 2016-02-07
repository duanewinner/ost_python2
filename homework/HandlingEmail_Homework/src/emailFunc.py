#!/usr/local/bin/python3

import os
import email
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText   
from email.mime.image import MIMEImage
import mimetypes

def emailFunc(recipient, message, attachments=None):

    a_errors = {}
    if not attachments:
        msg = email.message_from_string(message)
        msg['To'] = recipient
    else:
        msg = MIMEMultipart()
        msg['To'] = recipient
        text_msg = MIMEText(message, 'plain')
        msg.attach(text_msg)
        for fn in attachments:
            try:
                with open(fn, 'rb') as fp:
                    ctype, encoding = mimetypes.guess_type(fn)
                    # From: https://docs.python.org/3/library/email-examples.html
                    if ctype is None or encoding is not None:
                        # No guess could be made, or the file is encoded (compressed), so
                        # use a generic bag-of-bits type.
                        ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    #print(fn, ctype, encoding, maintype, subtype)
                    if maintype == "text":
                        attachment = MIMEText(fp.read(),_charset='us-ascii')
                    elif maintype == "image":
                        attachment = MIMEImage(fp.read())
                    elif maintype == "application":
                        attachment = MIMEApplication(fp.read())
                    else:
                        a_errors[fn] = "MIME Type \"" + maintype + "\" not supported"
                        continue
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fn))
                msg.attach(attachment)
            except FileNotFoundError:
                a_errors[fn] = "Attachment not found"
    if len(a_errors) == 0:
        a_errors = None
    return(msg, a_errors)



