#python2
from .. import ConfigParserEnc

class plugin:
        """Implements a plugin for SocialTray"""
        
        def __init__(self):   
                #Define name and icon
                self.name = ''
                self.icon = ''
                     
                #Load Configuration
                path = os.path.dirname(os.path.realpath(__file__))
                self.config = ConfigParser.RawConfigParser()
                self.config.read(os.path.realpath(path+'/tray.cfg'))
                
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
