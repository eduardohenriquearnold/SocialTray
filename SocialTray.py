#python2

import gtk
import imp
import os, sys, subprocess
import urllib2

import ConfigParserEnc
import timer

class SocialTray:
        '''Creates app with icon in notification area and display information about services'''

        def __init__(self):
                
                #load configuration
                self.config = ConfigParserEnc.ConfigParserEnc()
                self.config.read('tray.cfg')
                self.interval = float(self.config.get('tray','interval'))*60
                
                #import plugins 
                self.plugins = []                
                pluginsFolder = os.path.realpath(os.path.dirname(__file__)+'/plugins/')
                pluginsPath = [fname for fname in os.listdir(pluginsFolder) if fname.endswith('py')]

                for f in pluginsPath:
                        name = f.split('.')[0]
                        path = pluginsFolder+'/'+f
                        mod = imp.load_source(name, path)  
                        
                        if name != 'defaultPlugin':
                                self.plugins.append(mod.plugin())
                                setattr(self.plugins[-1], 'count', 0)
                                        
                #set icon and actions
                self.statusicon = gtk.StatusIcon()                
                self.set_icon('default')  
                self.statusicon.set_tooltip("Social Tray")                                                              
                self.statusicon.connect('popup-menu', self.on_right_click) 
                
                #start timer
                self.timer = timer.newTimer(self.update, self.interval)  
                
        def update(self):
                #Check internet connection
                if not self.internet_on():
                    return
                
                #Get and update count value for each plugin    
                for p in self.plugins:
                        newCount = p.getUnreadCount()
                        dif = newCount - p.count
                        setattr(p, 'count', newCount) 
                        
                        if dif>0:
                                self.set_icon('red')
                                
        def internet_on(self):
            try:
                response=urllib2.urlopen('http://google.com',timeout=1)
                return True
            except urllib2.URLError as err: pass
            return False                                                         
                
        def on_right_click(self, icon, event_button, event_time):
                self.set_icon('default')

                menu = gtk.Menu()
                
                #Plugins items
                for p in self.plugins:
                        Item = gtk.ImageMenuItem(str(p.count)+" unread")
                        Item.connect('activate', self.menu_click_new_tab, p.link)
                        Img = gtk.image_new_from_icon_name(p.icon, 17)
                        Item.set_image(Img)
                        menu.append(Item)                        				

                #Update
                Item = gtk.MenuItem("Update")
                Item.connect('activate', self.update)
                menu.append(Item)

                menu.show_all()
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.statusicon)

        def menu_click_new_tab(self, menu, link):
                subprocess.Popen(['xdg-open', link])

        def set_icon(self, name):
                if name is 'default':
                        iname = 'indicator-messages-new'
                elif name is 'red':
                        iname = 'new-messages-red'

                self.statusicon.set_from_icon_name(iname)

                                        
#Make possible to multithread with GTK
gtk.gdk.threads_init()

#Start app
SocialTray()
gtk.main()

                
        






        
