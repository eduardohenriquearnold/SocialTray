import facepy
import web, requests
import subprocess, threading
import defaultPlugin

class plugin(defaultPlugin.plugin):
        '''Facebook plugin class'''
        
        def loadConf(self):
                self.name = 'Facebook'
                self.icon = 'facebook'
                self.link = 'http://facebook.com/messages/'
                
                #Get app_id and app_secret from config file
                self.app_id = self.config.get('facebook','app_id')
                self.app_secret = self.config.get('facebook','app_secret')
                
                #Try to load token and use it. If it does not exist or is not recognized, generate a new one and write to config file
                try:
                        self.token = self.config.get('facebook','token')
                        self.graph = facepy.GraphAPI(self.token)
                        self.graph.fql('SELECT unread_count FROM mailbox_folder WHERE folder_id=0') 
                except:
                        self.getAuthToken()
                        self.config.set('facebook','token', self.token)
                        self.graph = facepy.GraphAPI(self.token)
                        
        def getUnreadCount(self):                      
                query = 'SELECT unread_count FROM mailbox_folder WHERE folder_id=0'
                                                           
                result = self.graph.fql(query)        
                count = result['data'][0]['unread_count']

                return count                       

        def getAuthToken(self):
                '''Get client token by Client Authentication and Authorization'''               

                post_login_url = "http://0.0.0.0:8080/"
                url = ('/', 'index')

                parentSelf = self
                                
                #Webpy Handler Class                
                class index:
                        def GET(self):
                                user_data = web.input(code=None)
                                code = user_data.code

                                if not code:
                                        dialog_url = ( "http://www.facebook.com/dialog/oauth?" +
                                                   "client_id=" + parentSelf.app_id +
                                                   "&redirect_uri=" + post_login_url +
                                                   "&scope=read_mailbox" )

                                        return "<script>top.location.href='" + dialog_url + "'</script>"
                                else:
                                        print(parentSelf.app_secret)
                                        print(parentSelf.app_id)
                                        token_url = ( "https://graph.facebook.com/oauth/access_token?" +
                                                  "client_id=" + parentSelf.app_id +
                                                  "&redirect_uri=" + post_login_url +
                                                  "&client_secret=" + parentSelf.app_secret +
                                                  "&code=" + code )
                                        response = requests.get(token_url).content

                                        params = {}
                                        result = response.split("&", 1)
                                        for p in result:
                                                (k,v) = p.split("=")
                                                params[k] = v

                                        access_token = params['access_token']  

                                        #Get extended token and write to parent class
                                        parentSelf.token = facepy.utils.get_extended_access_token(access_token, parentSelf.app_id, parentSelf.app_secret)[0]

                                        app.stop()
                                        return "<script>window.close();</script>"
                
                #Start Web.py application in new thread and open Browser            
                app = web.application(url, locals())
                th = threading.Thread(target=app.run)
                th.start()
                
                subprocess.Popen(['xdg-open', post_login_url])    
                th.join()
               

