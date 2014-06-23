import imaplib
import defaultPlugin

class plugin(defaultPlugin.plugin):

        def loadConf(self):
                #Define name, icon and link
                self.name = 'Gmail'
                self.icon = 'gmail'
                self.link = 'http://gmail.com'
                
                #Get user and password info                
                self.usr = self.config.get('gmail','username')
                self.psw = self.config.get('gmail','password') 
                                                               
        def getUnreadCount(self):
                '''Get the quantity of unread messages in Inbox of a Gmail Account'''

                obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
                obj.login(self.usr, self.psw)
                obj.select()

                n = len(obj.search(None, 'UnSeen')[1][0].split())        
                return n
                
        def getLink(self):
                return 
        

              

