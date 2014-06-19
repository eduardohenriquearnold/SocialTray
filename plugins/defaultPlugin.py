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
                #Define name and icon
                self.name = ''
                self.icon = ''
                     
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
                
        def getLink(self):
                """Return the link opened when the menu item is clicked"""
                pass
