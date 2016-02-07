#!/usr/local/bin/python3

import unittest
import emailFunc

class DBTest(unittest.TestCase):
    
    def test_1(self):
        msg, errors = emailFunc.emailFunc("duane@duanewinner.net","I have some attachments!",["python-logo.png","test.docx","test.xlsx.zip","test.txt","test.pdf"])
        mw = []
        msg.walk()
        for m in msg.walk():
            mw.append((m.is_multipart(), m.get_content_type())) 
        self.assertEqual(mw, ([(True, 'multipart/mixed'), (False, 'text/plain'), (False, 'image/png'), (False, 'application/octet-stream'), (False, 'application/octet-stream'), (False, 'text/plain'), (False, 'application/octet-stream')]))
        self.assertEqual(errors, None)

    def test_2(self):
        msg, errors = emailFunc.emailFunc("duane@duanewinner.net","I have some attachments!",["python-logo.png","test.docx","test.xlsx.zip","bogus.pdf","test.txt","xwing.wav","test.pdf"])
        mw = []
        msg.walk()
        for m in msg.walk():
            mw.append((m.is_multipart(), m.get_content_type())) 
        self.assertEqual(mw, ([(True, 'multipart/mixed'), (False, 'text/plain'), (False, 'image/png'), (False, 'application/octet-stream'), (False, 'application/octet-stream'), (False, 'text/plain'), (False, 'application/octet-stream')]))
        self.assertEqual(errors, {'bogus.pdf': 'Attachment not found', 'xwing.wav': 'MIME Type "audio" not supported'}) 

    def test_3(self):
        msg, errors = emailFunc.emailFunc("duane@duanewinner.net","I have some attachments!",["xwing.wav"])
        mw = []
        msg.walk()
        for m in msg.walk():
            mw.append((m.is_multipart(), m.get_content_type())) 
        self.assertEqual(mw, ([(True, 'multipart/mixed'), (False, 'text/plain')]))
        self.assertEqual(errors, {'xwing.wav': 'MIME Type "audio" not supported'}) 
        
    def test_4(self):
        msg, errors = emailFunc.emailFunc("duane@duanewinner.net","I have some attachments!",["test.docx", "bogus.docx"])
        mw = []
        msg.walk()
        for m in msg.walk():
            mw.append((m.is_multipart(), m.get_content_type())) 
        self.assertEqual(mw, ([(True, 'multipart/mixed'), (False, 'text/plain'), (False, 'application/octet-stream')]))
        self.assertEqual(errors, {'bogus.docx': 'Attachment not found'}) 

    def test_5(self):
        msg, errors = emailFunc.emailFunc("duane@duanewinner.net","No attachments today.")
        mw = []
        msg.walk()
        for m in msg.walk():
            mw.append((m.is_multipart(), m.get_content_type())) 
        self.assertEqual(mw, ([(False, 'text/plain')]))
        self.assertEqual(errors, None) 


if __name__ == "__main__":
    unittest.main()


