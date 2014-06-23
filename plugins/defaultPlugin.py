import os

##############################
#add parent folder to library
parentdir = os.path.abspath(__file__ + "/../../")
os.sys.path.insert(0,parentdir) 
##############################

from ConfigParserEnc import ConfigParserEnc

class plugin:
        """Implements a plugin for SocialTray"""
        
        def __init__(self):   
                #Define name, icon and link
                self.name = ''
                self.icon = ''
                self.link = ''
                     
                #Load Configuration
                self.config = ConfigParserEnc()
                self.config.read('tray.cfg')
                
                #Load particular information        
                self.loadConf()
        
        def loadConf(self):
                """Load the data the plugin may need from configuration file"""
                pass
                
        def getUnreadCount(self):                      
                pass
                
