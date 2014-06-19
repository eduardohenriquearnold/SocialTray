import os
from ConfigParser import RawConfigParser
from base64 import b64encode, b64decode

class ConfigParserEnc(RawConfigParser):
        """A config parser with encryption options that loads file from current directory"""
        
        def read(self, fname):
                folderPath = os.path.dirname(__file__)
                self.fPath = folderPath+'/'+fname
                
                RawConfigParser.read(self, self.fPath)
        
        def get(self, section, option):
                a = RawConfigParser.get(self, section, option) 
                               
                #Check if encoded
                if (a[0] == ':'):
                        dec = b64decode(a[1:])
                        return dec 
                else:
                        #Is the original string -> Encode and write to file
                        self.set(section, option, a)
                        return a                                                                       
                        
        def set(self, section, option, value):
                #The new value contains : in the beginning to indicate it's encoded
                nv = ':'+b64encode(value)
                RawConfigParser.set(self, section, option, nv)
                
                self.write(open(self.fPath, 'wb'))
                
        
