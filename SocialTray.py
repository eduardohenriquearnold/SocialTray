#python2

import gtk
import ConfigParserEnc

import os, subprocess
import timer

class SocialInfo:
        '''Implements data gathering from services'''

        def __init__(self):
                #Initial Values
                self.gCount = self.fCount = None

                #Load Configuration
                path = os.path.dirname(os.path.realpath(__file__))
                config = ConfigParser.RawConfigParser()
                config.read(os.path.realpath(path+'/tray.cfg'))

                self.gEn = config.get('gmail','enabled')
                self.gInt = int(config.get('gmail','interval'))*60
                self.gUser = config.get('gmail','username')
                self.gPass = config.get('gmail','password')

                self.fEn = config.get('facebook','enabled')
                self.fInt = int(config.get('facebook','interval'))*60

                #Start Threads
                if self.gEn == 'true':
                        timer.newTimer(self.countGmail, self.gInt)

                if self.fEn == 'true':
                        timer.newTimer(self.countFB, self.fInt)
                
        def countGmail(self):
                gCount = int(gmail.getInboxCount(self.gUser, self.gPass))
                self.update(gCount=gCount)

        def countFB(self):     
                fCount = int(facebook.getUnreadMessages())
                self.update(fCount=fCount)

        def update(self, gCount=None, fCount=None):
                if gCount != None:
                        self.gCount = gCount

                if fCount != None:
                        self.fCount = fCount

                print('UPDATE: gmail={0} face={1}'.format(self.gCount, self.fCount))


class SocialTray:
        '''Creates app with icon in notification area and display information about services'''

        def __init__(self):
                
                #load configuration
                self.config = ConfigParserEnc.ConfigParserEnc()
                self.config.read('tray.cfg')
                self.interval = float(self.config.read('tray','interval'))*60
                
                #import plugins 
                self.plugins = []
                

                #set icon and actions
                self.statusicon = gtk.StatusIcon()                
                self.set_icon('default')  
                self.statusicon.set_tooltip("Social Tray")
                                                              
                self.statusicon.connect('popup-menu', self.on_right_click)                                             
                
        def create_menu(self):
                menu = gtk.Menu()
                
                

        def on_right_click(self, icon, event_button, event_time):
                self.set_icon('default')

		menu = gtk.Menu()

		#Menu Items
                #Gmail
                gItem = gtk.ImageMenuItem(str(self.gCount)+" unread email")
                gItem.connect('activate', self.menu_click_new_tab, 'gmail.com')
                gImg = gtk.image_new_from_icon_name('gmail', 17)
                gItem.set_image(gImg)
                menu.append(gItem)

                #FB
                fItem = gtk.ImageMenuItem(str(self.fCount)+" unread messages")
                fItem.connect('activate', self.menu_click_new_tab, 'facebook.com')
                fImg = gtk.image_new_from_icon_name('facebook', 17)
                fItem.set_image(fImg)
                menu.append(fItem)

                #Update
                uItem = gtk.MenuItem("Update")
                uItem.connect('activate', self.menu_click_update)
                menu.append(uItem)

                menu.show_all()
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.statusicon)

        def menu_click_new_tab(self, menu, link):
                subprocess.Popen(['xdg-open', 'http://'+link])

        def menu_click_update(self, menu):
                self.countGmail()
                self.countFB()

        def set_icon(self, name):
                if name is 'default':
                        iname = 'indicator-messages-new'
                elif name is 'red':
                        iname = 'new-messages-red'

                self.statusicon.set_from_icon_name(iname)

        def update(self, gCount=None, fCount=None):
                #Solution for when internet is disabled (main process)
                if gCount != None:
                        if self.gCount != gCount and gCount > 0:
                                self.set_icon('red')

                        self.gCount = gCount

                if fCount != None:
                        if self.fCount != fCount and fCount > 0:
                                self.set_icon('red')
			
                        self.fCount = fCount
                                        
#Make possible to multithread with GTK
gtk.gdk.threads_init()

#Start app
SocialTray()
gtk.main()

                
        






        
