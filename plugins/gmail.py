#python2
# -*- coding: utf-8 -*-

import imaplib
import plugin from default

class gmail(plugin):

        def loadConf(self):
                #Define name and icon
                self.name = 'Gmail'
                self.icon = 'gmail'
                
                #Get user and password info                
                self.usr = config.get('gmail','username')
                self.psw = config.get('gmail','password') 
                                                               
        def getUnreadCount(self):
                '''Get the quantity of unread messages in Inbox of a Gmail Account'''

                obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
                obj.login(self.usr, self.psw)
                obj.select()

                n = len(obj.search(None, 'UnSeen')[1][0].split())        
                return n
                
        def getLink(self):
                return 'http://gmail.com'
        

              

