#python2
# -*- coding: utf-8 -*-

import imaplib

def getInboxCount(usr, psw):
        '''Get the quantity of unread messages in Inbox of a Gmail Account'''

        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        obj.login(usr,psw)
        obj.select()

        n = len(obj.search(None, 'UnSeen')[1][0].split())        
        return n
              

